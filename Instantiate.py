"""
version: 1.0
author: Santamaria Nicolas (chimps.lab)
website: https://github.com/besanta/UEPythonTools
license: LGPL
"""

import unreal
import sys
import traceback
from itertools import groupby
# https://docs.unrealengine.com/4.27/en-US/PythonAPI/
# https://sondreutheim.com/post/getting_started_with_python_in_ue4
# https://www.youtube.com/watch?v=UGnbx7iNMBQ&list=PLBLmKCAjA25Br8cOVzUroqi_Nwipg-IdP


# https://answers.unrealengine.com/questions/904813/python-attach-component-to-actor-or-blueunreal.log.html


def copyMaterials(src, dest):
	unreal.log(f' Set Materials')
	# materialIndex = 0
	# while True:
	# 	currentMaterial = first_mesh_component.static_mesh.get_material(materialIndex)
	# 	materialIndex = materialIndex + 1
	# 	if not currentMaterial:
	# 		break
	# 	# instance_component.static_mesh.set_material(materialIndex, currentMaterial)
	# 	instance_component.static_mesh.add_material(currentMaterial)
	# unreal.log(f'Done setting materials')
	
	# unreal.log(first_mesh_component.static_mesh.static_materials)
	# for i, m in enumerate(first_mesh_component.static_mesh.static_materials):
	# 	instance_component.static_mesh.set_material(i, m.material_interface)

def copyProps(dest, src, props):
	for p in props:
		dest.set_editor_property(p, src.get_editor_property(p))

def spawnHISM(actors):
	# actor_instance = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor)
	actor_bounds = unreal.GameplayStatics.get_actor_array_bounds(actors, False)[0]
	center_of_mass = actor_bounds
	if actors and len(actors):
		actor_instance = None
		try:
			unreal.log('Spawn actor')
			actor_class = unreal.EditorAssetLibrary.load_blueprint_class('/Game/BP_InstancedStaticMeshActor.BP_InstancedStaticMeshActor')
			actor_instance = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, center_of_mass)

			instance_component = actor_instance.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
			if instance_component:
				for sm in actors:
					instance_component.add_instance_world_space(sm.get_actor_transform())
				first_mesh_component = actors[0].static_mesh_component

				# Copy properties
				props_to_copy = ['static_mesh', 'override_materials', 'cast_shadow', 'mobility']
				copyProps(instance_component, first_mesh_component, props_to_copy)

			return actor_instance
		except Exception as err:
			unreal.log_error(f"Error during HISM Actor creation: \n\t {err}")
			if actor_instance:
				actor_instance.destroy_actor()
	return None

def cast(object_to_cast, object_class):
	try:
		return object_class.cast(object_to_cast)
	except:
		return None

def getSelectedActors(actor_class = None):
	selection = unreal.EditorLevelLibrary.get_selected_level_actors()
	class_actors = selection
	if actor_class:
		class_actors = [x for x in selection if cast(x, actor_class)]
		return class_actors
	return selection



selected_static_mesh = getSelectedActors(unreal.StaticMeshActor)
selected_static_mesh.sort(key= lambda x: x.static_mesh_component.static_mesh.get_path_name())

for x in selected_static_mesh:
	path = x.static_mesh_component.static_mesh.get_path_name()

for key, group in groupby(selected_static_mesh, lambda x: x.static_mesh_component.static_mesh.get_path_name()):
	items = list(group)
	# unreal.log(f'groups {key} with {len(items)} item(s)')
	# unreal.log(f'item(s): {items}')

	hism_actor = spawnHISM(items)
	if hism_actor:
		hism_component = hism_actor.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
		unreal.log(f'Spawned HISM for mesh {key} with {hism_component.get_instance_count} instances')
	else:
		unreal.log_error("Error during generation")

if sys.argv[1] == "-e":
	for x in selected_static_mesh:
		unreal.EditorLevelLibrary.destroy_actor(x)

unreal.EditorLevelLibrary.set_selected_level_actors(selected_static_mesh)