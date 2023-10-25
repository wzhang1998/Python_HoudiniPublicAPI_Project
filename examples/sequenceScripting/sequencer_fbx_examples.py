import unreal

'''
	Summary:
		This is an example of how to export fbx with animation  information with sequencer.  In this example we load a map and corresponding level sequence,
		grab all of the bindings from that sequence, set some export options, then export the fbx file.
		To save less you need to only choose those bindings you want to export. 
		Open the Python interactive console and do similarly as below:
			import sequencer_fbx_examples
			sequencer_fbx_examples.export_fbx("/Game/Maps/FbxTest","/Game/FbxTest", "/Game/FbxTest_Root", "D:\\FBX_Test.fbx")
		
	Params:
	    map_asset_path - String that points to the map that conatains the possessables contained in the Movie Scene sequence.
		sequencer_asset_path - String that points to the Movie Scene sequence asset.
		root_sequencer_asset_path - String that points to the root sequence that this sequence is a part of. If none, just specify the sequencer_asset_path
        output_file - String that shows the full path of the created fbx file.
'''
def export_fbx(map_asset_path, sequencer_asset_path, root_sequencer_asset_path, output_file):
	# Load the map, get the world
	world = unreal.EditorLoadingAndSavingUtils.load_map(map_asset_path)
	# Load the sequence asset
	sequence = unreal.load_asset(sequencer_asset_path, unreal.LevelSequence)
	root_sequence = unreal.load_asset(root_sequencer_asset_path, unreal.LevelSequence)
	# Set Options
	export_options = unreal.FbxExportOption()
	export_options.ascii = True
	export_options.level_of_detail = False
	# Get Bindings
	bindings = sequence.get_bindings()
	tracks = sequence.get_tracks()
	# Export
	export_fbx_params = unreal.SequencerExportFBXParams(world, sequence, root_sequence, bindings, tracks, export_options, output_file)
	unreal.SequencerTools.export_level_sequence_fbx(export_fbx_params)

	return

'''
	Summary:
		This is an example of how to import fbx including animation onto a sequencer level sequence.  In this example we create sequencer asset, use passed in
		actor labels to create bindings in the sequence, then import the fbx onto these bindings.
		Open the Python interactive console and use:
			import sequencer_fbx_examples
			label_list = ["Floor"]  #Assuming that we have a Floor in the scene and the Fbx file has animation loading onto a Floor Node.
			sequencer_fbx_examples.import_fbx("/Game/Maps/FbxTest","NewFbxTest", "/Game/",label_list, "D:\\FBX_Test.fbx")
		
	Params:
	        map_asset_path - String that points to the Map that conatains the possessables contained in the Movie Scene sequence.
		sequencer_asset_name - String that is our level sequence name.
		package_path - String to path to create the level sequence asset.
		actor_label_list - Array of actor labels that we want to creete tracks for and then import onto.
		input_fbx_file - String that shows the full path of the imported fbx file.
'''
def import_fbx(map_asset_path, sequencer_asset_name, package_path, actor_label_list, input_fbx_file):
        
	# Load the map, get the world
	world = unreal.EditorLoadingAndSavingUtils.load_map(map_asset_path)
	# Get Actors from passed in names
	level_actors = unreal.EditorLevelLibrary.get_all_level_actors()
	actor_list = []
	for label in actor_label_list:
		filtered_list = unreal.EditorFilterLibrary.by_actor_label(level_actors, label,unreal.EditorScriptingStringMatchType.EXACT_MATCH)
		actor_list.extend(filtered_list)
	# Create the sequence asset
	sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(sequencer_asset_name, package_path, unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
	# Create Bindings
	for actor in actor_list:
		sequence.add_possessable(actor)
	bindings = sequence.get_bindings()
	# Set Options
	import_options = unreal.MovieSceneUserImportFBXSettings()
	#import_options.set_editor_property("create_cameras",True)
	import_options.set_editor_property("reduce_keys",False)

	# Import
	unreal.SequencerTools.import_level_sequence_fbx(world, sequence, bindings, import_options, input_fbx_file)

	return sequence

'''
	Summary:
		This is an example of how to import fbx including animation onto an existing template sequence. The template sequence must already be bound to the correct type of actor and the actor must have all the components that are necessary for the imported properties
		Open the Python interactive console and use:
			import sequencer_fbx_examples
			sequencer_fbx_examples.import_fbx_onto_template_sequence('/Game/NewMap', '/Game/NewTemplateSequence', 'D:///testcam.fbx')
		
	Params:
	    map_asset_path - String that points to the Map that conatains the possessables contained in the Movie Scene sequence.
		template_asset-path - String that is our template sequence name.
		input_fbx_file - String that shows the full path of the imported fbx file.
'''
def import_fbx_onto_template_sequence(map_asset_path, template_asset_path, input_fbx_file):
	# Load the map, get the world
	world = unreal.EditorLoadingAndSavingUtils.load_map(map_asset_path)
	template_sequence = unreal.load_asset(template_asset_path, unreal.TemplateSequence)
	bindings = template_sequence.get_bindings()
	# Set Options
	import_options = unreal.MovieSceneUserImportFBXSettings()
	#import_options.set_editor_property("create_cameras",True)
	import_options.set_editor_property("reduce_keys",False)
	# Import
	unreal.SequencerTools.import_template_sequence_fbx(world, template_sequence, bindings, import_options, input_fbx_file)
	return template_sequence


'''
	Summary:
		This is an example of how to import fbx animation onto a control rig sequencer track.
		In this example we load a map, load a sequencer asset that contains a control rig track driving an actor in that map,
		specify the name of that actor/track in the sequence that we want to import onto, and then specify the location of the fbx file.
		The function itself shows how to use the option object to specify more options as needed.
		Open the Python interactive console and use:
			import sequencer_fbx_examples
			sequencer_fbx_examples.import_fbx_onto_control_rig("/Game/Maps/FbxImportTestMap","/Game/Maps/FbxImportTest", "ControlTest", "D:\\Test.fbx")
		
	Params:
	        map_asset_path - String that points to the Map with the control rig actor
		sequencer_asset_path - String that points to the path of the sequence with the control rig track.
		control_rig_actor_label - The name of that control rig track.
		input_fbx_file - String that shows the full path of the imported fbx file.
'''
def import_fbx_onto_control_rig(map_asset_path, sequencer_asset_path, control_rig_actor_label, input_fbx_file):
        
	# Load the map, get the world
	world = unreal.EditorLoadingAndSavingUtils.load_map(map_asset_path)
	# Load the Sequencer asset
	sequence = unreal.load_asset(sequencer_asset_path, unreal.LevelSequence)
	unreal.LevelSequenceEditorBlueprintLibrary().open_level_sequence(sequence)	
	# Set Options
	import_options = unreal.MovieSceneUserImportFBXControlRigSettings()
	find_replace = unreal.ControlFindReplaceString()
	find_replace.set_editor_property("find","pSphere1")
	find_replace.set_editor_property("replace","Float")
	strings = import_options.get_editor_property("find_and_replace_strings")
	strings.append(find_replace)
	import_options.set_editor_property("find_and_replace_strings",strings)
	# Selected control rig contols, use MovieSceneUserImportFBXControlRigSettings.set_editor_property("import_onto_selected_controls",true)
	# if want to just import onto them
	selected_controls = []
	# Import
	unreal.SequencerTools.import_fbx_to_control_rig(world, sequence,control_rig_actor_label, selected_controls,import_options, input_fbx_file)

	return sequence



