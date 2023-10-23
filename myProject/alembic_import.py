import unreal

# Create an Alembic import task
# str variable current_abc_path is created from back alembic command in unreal EUW

task = unreal.AssetImportTask()
task.filename =  current_abc_path 
task.destination_path = r"/Game/ABC"
task.automated = True
task.replace_existing = True
task.async_ = True

# Set the import settings for Alembic
alembic_settings = unreal.AbcImportSettings()

# Customize Alembic import settings here if needed
alembic_settings.import_type = unreal.AlembicImportType.GEOMETRY_CACHE

alembic_settings.conversion_settings = unreal.AbcConversionSettings(
		scale=unreal.Vector(100, -100, 100),  # Set the scale using a Vector (adjust the values accordingly)
    rotation=unreal.Vector(90, 0.0, 0.0)  # Set the rotation using a Vector (adjust the values accordingly)
)

# Assign the Alembic settings to the import task
task.options = alembic_settings

# Execute the import task
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

print("Alembic import completed successfully!")

# Get the current level
current_level = unreal.EditorLevelLibrary.get_editor_world()
importedObject = task.get_objects()

# Create an Alembic actor using spawn_actor_from_object
alembic_actor = unreal.EditorLevelLibrary.spawn_actor_from_object(importedObject[0], unreal.Vector(0, 0, 0))

level_sequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

# Get the Actor and Level Sequence Editor subsystems

actor_system = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

ls_system = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)

# Add selected actors to current level sequence as possessables

GeoCacheActors = unreal.EditorFilterLibrary.by_class(actor_system.get_all_level_actors(), unreal.GeometryCacheActor)

bindings = ls_system.add_actors(GeoCacheActors)

# Use the binding to add tracks into sequencer - specified by track type

geo_track = bindings[0].add_track(unreal.MovieSceneGeometryCacheTrack)

# Add section to track to be able to manipulate range, parameters, or properties

geo_section = geo_track.add_section()

# Get level sequence start and end frame

start_frame = level_sequence.get_playback_start()

end_frame = level_sequence.get_playback_end()

# Set section range to level sequence start and end frame

geo_section.set_range(start_frame, end_frame)