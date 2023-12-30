import unreal
from pathlib import Path
# Create an Alembic import task
# str variable current_abc_path is created from back alembic command in unreal EUW

ABC_SOURCE_DIR = Path("D:\\Efiles\\Unreal Projects\\20231206_FX_test\\HDARender")
VALID_EXTS = (".abc")
DEST_DIR_UE = r"/Game/ABC"
SAVE_FREQ = 5 # save every 5 assets imported
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()


# Set the import settings for Alembic
alembic_settings = unreal.AbcImportSettings()

# Customize Alembic import settings here if needed
alembic_settings.import_type = unreal.AlembicImportType.GEOMETRY_CACHE

alembic_settings.conversion_settings = unreal.AbcConversionSettings(
    scale=unreal.Vector(100, -100, 100),  # Set the scale using a Vector (adjust the values accordingly)
    rotation=unreal.Vector(90, 0.0, 0.0)  # Set the rotation using a Vector (adjust the values accordingly)
)

path_to_import = list()
for file_path_abs in ABC_SOURCE_DIR.iterdir():
     if file_path_abs.suffix not in VALID_EXTS:
            continue
     path_to_import.append(file_path_abs)

num_assets_to_save= 0
with unreal.ScopedSlowTask(len(path_to_import), "Batch importing Alembic files") as slow_task:
    slow_task.make_dialog(True) 
    for file_path_abs in path_to_import:
        if slow_task.should_cancel():
            break
        slow_task.enter_progress_frame(1)

        if file_path_abs.suffix not in VALID_EXTS:
            continue
        name = file_path_abs.stem
        file_name_parts = name.split("_")
        file_name_start = file_name_parts[0]
        only_letters = [ch for ch in file_name_start if ch.isalpha()]
        tex_category = "".join(only_letters)


        task = unreal.AssetImportTask()
        task.filename =  str(file_path_abs)
        task.destination_path = DEST_DIR_UE
        task.automated = True
        task.replace_existing = True
        task.async_ = True
        task.save = False

        
        # Assign the Alembic settings to the import task
        task.options = alembic_settings

        # Execute the import task
        asset_tools.import_asset_tasks([task])

        num_assets_to_save += 1
        if num_assets_to_save >= SAVE_FREQ:
            unreal.EditorLoadingAndSavingUtils.save_dirty_packages(
                save_map_packages=False, save_content_packages=True
            )
            num_assets_to_save = 0



print("Alembic import completed successfully!")