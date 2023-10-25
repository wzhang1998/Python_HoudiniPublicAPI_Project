import unreal

# get current world and levelsequence
world = unreal.EditorLevelLibrary.get_editor_world()
level_sequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

# remove bound objects and their tracks if their name ends with "_output"
bound_objects = unreal.SequencerTools().get_bound_objects(world, level_sequence,level_sequence.get_bindings(), level_sequence.get_playback_range())
for bound_object in bound_objects:
    if str(bound_object.binding_proxy.get_display_name()).endswith("_output"):
        tracks=bound_object.binding_proxy.get_tracks()
        for track in tracks:
                bound_object.binding_proxy.remove_track(track)
        bound_object.binding_proxy.remove()
        unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()


actor_system = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ls_system = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)

# delete all geocache actors from current level
GeoCacheActors = unreal.EditorFilterLibrary.by_class(actor_system.get_all_level_actors(), unreal.GeometryCacheActor)

actor_system.destroy_actors(GeoCacheActors)