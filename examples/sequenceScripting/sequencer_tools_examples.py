# Import the Unreal module to gain access to the UObject/UStruct types.
import unreal

# Ensure you have enabled both the "Python Editor Script Plugin" and the "SequencerScripting" plugins for these examples to work.

'''
	Summary:
		Bake transform for all of the bindings of the given sequence. 
        Ensure you have enabled both the "Python Editor Script Plugin" and the "SequencerScripting" plugin in your project.
		Open the Python interactive console and use:
			import sequencer_tools_examples
			sequencer_tools_examples.bake_transform("/Game/TestSequence")
		
	Params:
		sequencer_asset_path - String that points to the Movie Scene sequence asset we should load and bake.
'''
def bake_transform(sequencer_asset_path):

    sequence = unreal.load_asset(sequencer_asset_path, unreal.LevelSequence)	
    bindings = sequence.get_bindings()

    # Bake from the playback start to the playback end per frame    
    bake_in_time = unreal.FrameTime(unreal.FrameNumber(sequence.get_playback_start()))
    bake_out_time = unreal.FrameTime(unreal.FrameNumber(sequence.get_playback_end()))
    bake_interval = unreal.FrameTime(unreal.FrameNumber(1))
        
    level_sequence_editor_subsystem = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)
    level_sequence_editor_subsystem.bake_transform(bindings, bake_in_time, bake_out_time, bake_interval)