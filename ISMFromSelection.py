"""
version: 1.0
author: Santamaria Nicolas (chimps.lab)
website: https://github.com/besanta/UEPythonTools
license: LGPL
"""

import unreal
import sys
# https://docs.unrealengine.com/4.27/en-US/PythonAPI/
# https://sondreutheim.com/post/getting_started_with_python_in_ue4
# https://www.youtube.com/watch?v=UGnbx7iNMBQ&list=PLBLmKCAjA25Br8cOVzUroqi_Nwipg-IdP
# https://answers.unrealengine.com/questions/904813/python-attach-component-to-actor-or-blueunreal.log.html

class_to_load = '/Game/BP_InstancedStaticMeshActor.BP_InstancedStaticMeshActor'

tag_to_search = ''
if "-t" in sys.argv:
	tagindex = sys.argv.index('-t')
	tag_to_search = sys.argv[tagindex + 1]

def help():
	print("ISMFromSelection.py\n\n\
	short:\n\
		Select Actors in Level and create a InstancedStaticMeshActor with all transforms of the selection\n\
	args:\n\
		-p	Define Prototype of the actor type (ex: Blueprint'/Game/BP_InstancedStaticMeshActor.BP_InstancedStaticMeshActor')\n\
		-t	Search for SceneComponent with tag. Will add all WorldTransform of each tagged Components to ISM.\
		-s	Search for StaticMeshComponent and add (the first found) to ISM.\
		-h	Print this help\n\
	")

def spawnHISM(actors):
	# actor_instance = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor)
	actor_bounds = unreal.GameplayStatics.get_actor_array_bounds(actors, False)[0]
	center_of_mass = actor_bounds
	if actors and len(actors):
		actor_instance = None
		try:
			unreal.log('Spawn actor')
			actor_class = unreal.EditorAssetLibrary.load_blueprint_class(class_to_load)
			actor_instance = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, center_of_mass)

			instance_component = actor_instance.get_component_by_class(unreal.InstancedStaticMeshComponent)
			if instance_component:
				for sm in actors:
					if "-s" in sys.argv:
						static_mesh_component = sm.get_component_by_class(unreal.StaticMeshComponent)
						instance_component.add_instance_world_space(static_mesh_component.get_world_transform())
					if "-t" in sys.argv:
						scene_components = sm.get_components_by_tag(unreal.SceneComponent, tag_to_search)
						unreal.log("  Fount %d components with tag %s" % (len(scene_components), tag_to_search))
						for sc in scene_components:
							instance_component.add_instance_world_space(sc.get_world_transform())
					else:
						instance_component.add_instance_world_space(sm.get_actor_transform())
			return actor_instance
		except Exception as err:
			unreal.log_error("Error during ISM Actor creation: \n\t %s" % err)
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

def execute():
	selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()

	hism_actor = spawnHISM(selected_actors)
	if hism_actor:
		hism_component = hism_actor.get_component_by_class(unreal.InstancedStaticMeshComponent)
		unreal.log('Spawned ISM with %d instances' % hism_component.get_instance_count())
	else:
		unreal.log_error("Error during generation")
	unreal.EditorLevelLibrary.set_selected_level_actors(selected_actors)

try:
	if '-p' in sys.argv:
		pindex = sys.argv.index('-p')
		class_to_load = sys.argv[pindex + 1]

	if '-h' in sys.argv:
		help()
	else:
		execute()
except Exception as err:
	unreal.log_error(err)
	help()