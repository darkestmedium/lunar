# Built-in imports

# Third-party imports
import unreal as uep

# Custom imports

# Class instances
editor_util = uep.EditorUtilityLibrary()
system_lib = uep.SystemLibrary()


# Prefixes 
prefix_mapping = {
	# General
  "HDRI": "HDR_",
  "Material": "M_",
	"MaterialFunction": "MF_",
  "MaterialInstanceConstant": "MI_",
  "PhysicsAsset": "PHYS_",
  "PhysicsMaterial": "PM_",
  "PostProcessMaterial": "PPM_",
  "SkeletalMesh": "SK_",
  "StaticMesh": "SM_",
  "Texture2D": "T_",
  "OCIOProfile": "OCIO_",

	# Blueprints
  "ActorComponent": "AC_",
  "AnimBlueprint": "ABP_",
  "Blueprint": "BP_",
  "BlueprintInterface": "BI_",
	"CurveTable": "CT_",
	"DataTable": "DT_",
	"Enum": "E_",
	"Structure": "S_",
  "WidgetBlueprint": "WBP_",

	# Particle Effects
	"ParticleSystem": "PS_",
	"NiagaraEmiitter": "FXE_",
	"NiagaraSystem": "FXS_",
	"NiagaraFunction": "FXF_",

	# Skeletal Mesh Animations
  "ControlRigBlueprint": "CR_",
  "IKRigDefinition": "IKRD_",
  "IKRetargeter": "RTG_",
  "Skeleton": "SKEL_",
  "AnimMontage": "AM_",
  "AnimSequence": "AS_",
  "BlendSpace": "BS_",
  "BlendSpace1D": "BS_",

	# ICVFX
	"NDisplayConfiguration": "NDC_",

	# Animation
	"LevelSequence": "LS_",
	"CameraAnimationSequence": "CAS_",
	"TemplateSequence": "TS_",
	"SequencerEdits": "EDIT_",

	# Media
	"MediaSource": "MS_",
	"MediaOutput": "MO_",
	"MediaPlayer": "MP_",
	"MediaProfile": "MPR_",

	# Other
	"LevelSnapshot": "SNAP_",
	"RemoteControlPreset": "RCP_",

	# Sound
  "SoundCue": "SC_",
  "SoundWave": "S_",

  "MorphTarget": "MT_",
  "RenderTarget": "RT_",
  "World": "LVL_",
	# Textures
  "TextureRenderTarget2D": "TRT_",
}



# get the selected assets
selected_assets = editor_util.get_selected_assets()
num_assets = len(selected_assets)
prefixed = 0

if num_assets != 0:
	# do the renaiming

	for asset in selected_assets:
		# get the class instance and the clear text name
		asset_name = system_lib.get_object_name(asset)
		asset_class = asset.get_class()
		class_name = system_lib.get_class_display_name(asset_class)

		# get the prefix for the given class
		class_prefix = prefix_mapping.get(class_name, None)

		if class_prefix is None:
			uep.log_warning(f"No mapping for asset {asset_name} of type {class_name}")
			continue

		if not asset_name.startswith(class_prefix):
			# rename the asset and add prefix
			new_name = class_prefix + asset_name
			editor_util.rename_asset(asset, new_name)
			prefixed += 1
			uep.log(f"Prefixed {asset_name} of type {class_name} with {class_prefix}")

		else:
			uep.log(f"Asset {asset_name} of type {class_name} is already prefixed with {class_prefix}")

	uep.log(f"Prefixed {prefixed} of {num_assets} assets")

else:
	uep.log_warning("No assests were selected.")
