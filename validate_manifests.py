"""Validate all package, asset, and integration manifests across all bundles"""

import base64
import glob
import json
import os
import sys
import six
from semantic_version import Version
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO, BytesIO
from collections import defaultdict

from difflib import SequenceMatcher
import jsonschema
from PIL import Image

DEPLOY_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(DEPLOY_DIR)
BUNDLE_DIR = os.path.join(PROJECT_DIR, 'src')

ASSET_IMG_SIZE = (150, 100)
INTEGRATION_IMG_SIZE = (86, 86)
SRC_IMG_SIZE = (240, 240)


def get_schema_validator(filename):
    """Return jsonschema validator populated from provided schema file"""
    with open(os.path.join(DEPLOY_DIR, 'schemas', filename)) as f:
        return jsonschema.Draft4Validator(json.load(f))


integrations_schema_validator = get_schema_validator('integration.schema.json')
asset_schema_validator = get_schema_validator('asset.schema.json')
package_schema_validator = get_schema_validator('package.schema.json')


def validate_manifest(manifest_data, validator):
    """Validate provided manifest_data against validator, returning list of all raised exceptions during validation"""
    return list(validator.iter_errors(manifest_data))


def check_asset_inputs_for_static_keys(inputs, validation_exceptions):

    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    for item in inputs:
        if similar(item.lower(), 'http_proxy') > .84 and item != 'http_proxy':
            validation_exceptions.append(ValueError('Pro xy keys must be named "http_proxy", you provided {}'.format(item)))

        if (similar(item.lower(), 'verify_ssl') > .84 or similar(item.lower(), 'ssl_verify') > .84) and item != 'verify_ssl':
            validation_exceptions.append(ValueError('Verify SSL keys must be named "verify_ssl", you provided {}'.format(item)))

    return validation_exceptions


def validate_asset_manifest(asset_manifest, bundle_path):
    """Validate asset manifest data, return list of all exceptions raised during validation"""

    validation_exceptions = validate_manifest(asset_manifest, asset_schema_validator)

    validation_exceptions = check_asset_inputs_for_static_keys(asset_manifest['inputParameters'], validation_exceptions)

    test_script_file = asset_manifest.get('testScriptFile')
    if test_script_file:
        if not os.path.isfile(os.path.join(bundle_path, 'imports', test_script_file)):
            validation_exceptions.append(ValueError(
                'Unable to find testScriptFile "{}" in bundle path "{}"'.format(
                    test_script_file,
                    bundle_path
                )
            ))

    return validation_exceptions


def validate_integration_manifest(integration_manifest, package_manifest, asset_manifest, bundle_path):
    """Validate loaded integration JSON manifest data, returns list of all exceptions raised during validation"""
    # Validate against JSONschema for expected structure
    validation_exceptions = validate_manifest(integration_manifest, integrations_schema_validator)

    # Verify integration version matches package version
    integration_version = integration_manifest['version']
    package_version = package_manifest['version']
    if integration_version != package_version:
        validation_exceptions.append(ValueError('Integration version "{}" != Package version "{}"'.format(
            integration_version,
            package_version
        )))

    # Verify asset dependency matches asset provided by bundle with expected type and version
    asset_dep_type = integration_manifest.get('assetDependencyType')
    asset_dep_version = integration_manifest.get('assetDependencyVersion')
    if asset_dep_type:
        # Check type
        asset_type = asset_manifest['type']
        if asset_dep_type != asset_type:
            validation_exceptions.append(
                ValueError('Integration depends on wrong asset type "{}", bundle provides "{}"'.format(
                    asset_dep_type,
                    asset_type
                ))
            )

        # Check version
        asset_version = asset_manifest['version']
        if asset_dep_version != asset_version:
            validation_exceptions.append(
                ValueError('Integration depends on wrong asset version "{}", bundle provides "{}"'.format(
                    asset_dep_version,
                    asset_version
                ))
            )
    elif asset_dep_version:
        # Check no dependency version set when no asset type specified
        validation_exceptions.append(
            ValueError('Integration specifies assetDependencyVersion without assetDependencyType')
        )

    # Verify scriptFile exists
    script_file = integration_manifest['scriptFile']
    if not os.path.isfile(os.path.join(bundle_path, 'imports', script_file)):
        validation_exceptions.append(
            ValueError('Unable to find scriptFile "{}" in bundle path "{}"'.format(
                script_file,
                bundle_path
            ))
        )

    # Base64 to Pillow Image object helper func
    def get_img(b64):

        try: # Py2
            tmp_f = StringIO()
            tmp_f.write(base64.b64decode(b64.split(",")[1]))
        except:
            tmp_f = BytesIO()
            tmp_f.write(base64.b64decode(b64.split(",")[1]))
        tmp_f.seek(0)
        return Image.open(tmp_f)

    # Verify base64Image of asset and integration is the correct size
    if asset_manifest != {}:
        asset_img = get_img(asset_manifest["base64Image"])
        if asset_img.size != ASSET_IMG_SIZE:
            validation_exceptions.append(ValueError("Asset image is {ax}x{ay}, expected {ex}x{ey}".format(
                 ax=asset_img.size[0], ay=asset_img.size[1], ex=ASSET_IMG_SIZE[0], ey=ASSET_IMG_SIZE[1]
            )))

    integration_img = get_img(integration_manifest["base64Image"])
    if integration_img.size != INTEGRATION_IMG_SIZE:
        validation_exceptions.append(ValueError("Integration image is {ix}x{iy}, expected {ex}x{ey}".format(
            ix=integration_img.size[0], iy=integration_img.size[1],
            ex=INTEGRATION_IMG_SIZE[0], ey=INTEGRATION_IMG_SIZE[1]
        )))

    src_logo_path = os.path.join(bundle_path, "image", "logo.png")
    if os.path.exists(src_logo_path):
        src_img = Image.open(src_logo_path)
        if src_img.size != SRC_IMG_SIZE:
            validation_exceptions.append(ValueError("Source image is {sx}x{sy}, expected {ex}x{ey}".format(
                sx=src_img.size[0], sy=src_img.size[1],
                ex=SRC_IMG_SIZE[0], ey=SRC_IMG_SIZE[1]
            )))
    else:
        validation_exceptions.append(ValueError("Can't find image/logo.png!"))

    return validation_exceptions


def get_integration_manifest_paths(bundle_path):
    """Return absolute paths for all integration manifest files from bundles in src/ directory"""
    return [m for m in glob.glob(os.path.join(bundle_path, 'imports', '*.json')) if not m.endswith('asset.json')]


def get_bundle_paths():
    """Return absolute paths to all bundles"""
    return filter(os.path.isdir, (os.path.join(BUNDLE_DIR, p) for p in os.listdir(BUNDLE_DIR)))


def get_py_files(bundle_path, package_name):
    py_files = []
    [py_files.append(m) for m in glob.glob(os.path.join(bundle_path, 'imports', '*.py'))]
    # Don't forget init.py
    py_files += glob.glob(os.path.join(bundle_path, package_name, '__init__.py'))
    return py_files


def check_for_context(py_files, failures, bundle_path):
    for f in py_files:
        with open(f, 'r') as p:
            text = p.read()
            if "class Context" in text:
                failures[bundle_path].append(ValueError('Context statement found in file: "{}"'.format(p)))


def _open(meta, mode='r'):
    try:
        return open(meta, mode, encoding='utf-8')
    except:
        return open(meta, mode)

def main():
    print('Validating manifests for bundles in "{}"'.format(BUNDLE_DIR))

    failures = defaultdict(list)

    # Collect names to prevent duplicates
    package_names = set()
    asset_names = set()
    integration_names = set()
    ui_name_set = set()
    for bundle_path in get_bundle_paths():

        print('Validating bundle at "{}"'.format(bundle_path))

        if not os.path.exists(os.path.join(bundle_path, 'README.md')):
            failures[bundle_path].append(ValueError('No README.md found "{}"'.format(bundle_path)))
        else:
            with open(os.path.join(bundle_path, "README.md")) as f:
                if "!*CHANGEME*!" in f.read():
                    failures[bundle_path].append(ValueError('README.md not updated "{}"'.format(bundle_path)))

        if not os.path.exists(os.path.join(bundle_path, "CHANGELOG.md")):
            failures[bundle_path].append(ValueError('No CHANGELOG.md found "{}"'.format(bundle_path)))
        else:
            with open(os.path.join(bundle_path, "CHANGELOG.md")) as f:
                if "* !*CHANGEME*!" in f.read():
                    failures[bundle_path].append(ValueError('CHANGELOG.md not updated "{}"'.format(bundle_path)))

        package_path = os.path.join(bundle_path, 'package.json')
        with open(package_path) as f:
            package_manifest = json.load(f)

        asset_path = os.path.join(bundle_path, 'imports/asset.json')
        with open(asset_path) as f:
            asset_manifest = json.load(f)

        # Package
        package_name = package_manifest['name']
        if package_name in package_names:
            failures[package_path].append(ValueError('Duplicate bundle name "{}"'.format(package_name)))
        if package_manifest.get('python_version') == '3.6' and not Version(package_manifest.get('supported_swimlane_version', "0.0.1").replace(">=", "")) >= Version("10.0.0"):
            failures[package_path].append(ValueError('Python 3 requires `supported_swimlane_version>=10.0.0`'))
        package_names.add(package_name)

        failures[package_path] += validate_manifest(package_manifest, package_schema_validator)

        ui_name = "{} {}".format(package_manifest['vendor'], package_manifest['product'])
        if package_manifest['vendor'] == package_manifest['product']:
            ui_name = package_manifest['vendor']
        if ui_name in ui_name_set:
            failures[package_path].append(ValueError('Duplicate Vendor and Product "{}"'.format(ui_name)))
        else:
            ui_name_set.add(ui_name)

        # Asset
        # Ignore empty assets
        if asset_manifest != {}:
            asset_name = asset_manifest['name']
            if asset_name in asset_names:
                failures[asset_path].append(ValueError('Duplicate asset name "{}"'.format(asset_name)))
            asset_names.add(asset_name)

            failures[asset_path] = validate_asset_manifest(asset_manifest, bundle_path)

        # Integrations
        for integration_manifest_path in get_integration_manifest_paths(bundle_path):
            with _open(integration_manifest_path) as f:
                try:
                    integration_manifest = json.load(f)
                except Exception as e:
                    raise Exception("Error in file \'" + f.name + "\' " + str(e))

            integration_name = integration_manifest['actionType']
            if integration_name in integration_names:
                failures[integration_manifest_path].append(
                    ValueError('Duplicate integration name "{}"'.format(integration_name))
                )
            else:
                integration_names.add(integration_name)

            failures[integration_manifest_path] += validate_integration_manifest(
                integration_manifest,
                package_manifest,
                asset_manifest,
                bundle_path
            )

        # Check for Context in each py file.
        py_files = get_py_files(bundle_path, package_name)
        check_for_context(py_files, failures, bundle_path)

    # Collect and report all failures across all manifests
    total_failures = sum([len(errors) for errors in six.itervalues(failures)])

    if total_failures:
        failure_message = '{} total failure(s) validating manifests'.format(total_failures)
        print(failure_message)
        print('-' * 120)
        for path, errors in sorted(six.iteritems(failures)):
            if errors:
                print(path + ' - Total Error(s): {}'.format(len(errors)))
                for error in errors:
                    print(' * ' + error.__class__.__name__ + ' - ' + str(error))
                print('-' * 120)
        print(failure_message)

    else:
        print('All manifests successfully validated')

    sys.exit(total_failures > 0)


if __name__ == '__main__':
    main()