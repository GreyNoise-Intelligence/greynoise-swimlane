from swimlane import Swimlane

# Stores the Personal Access Token needed to use the driver
pat = sw_context.inputs['pat']

# Establishes a Swimlane Drive Connection
swimlane = Swimlane(sw_context.config['InternalSwimlaneUrl'], access_token=pat, verify_ssl=False)
# Defines the Application ID where the GreyNoise Lookups are being done
lookup_app = swimlane.apps.get(id=sw_context.config['ApplicationId'])
# Defines the Application Name where the GreyNoise Tags are stored.
# This value should be updated if the name is different
tags_app = swimlane.apps.get(name='GreyNoise Tags')
# Grabs the record ID of the current Record
record = lookup_app.records.get(id=sw_context.config['RecordId'])
# Gathers the list of Tags on the record.
# This value should be updated if the name is different
tag_list_cursor = record['GN Tags']
if tag_list_cursor:
    for tag in tag_list_cursor:
        # Searches for the associated Tag Records in the Tag App.
        # This value should be updated if the name is different
        tag_record = tags_app.records.search(('GN Tag Name', 'equals', tag))
        # Attaches the first Tag record returned in the search to the current record.
        # This value should be updated if the name is different
        record['Tag Reference'].add(tag_record[0])
    # Patches the record ones all the references are added.
    record.patch()
