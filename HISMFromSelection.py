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

def spawnHISM(actors):
	# actor_instance = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor)
	actor_bounds = unreal.GameplayStatics.get_actor_array_bounds(actors, False)[0]
	center_of_mass = actor_bounds
	if actors and len(actors):
		actor_instance = None
		try:
			unreal.log('Spawn actor')
			actor_class = unreal.EditorAssetLibrary.load_blueprint_class('/Game/Actors/ActorsTools/BP_HISM.BP_HISM')
			actor_instance = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, center_of_mass)

			instance_component = actor_instance.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
			if instance_component:
				for sm in actors:
					instance_component.add_instance_world_space(sm.get_actor_transform())
			return actor_instance
		except Exception as err:
			unreal.log_error("Error during HISM Actor creation: \n\t %s", err)
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

selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()

hism_actor = spawnHISM(selected_actors)
if hism_actor:
	hism_component = hism_actor.get_component_by_class(unreal.HierarchicalInstancedStaticMeshComponent)
	unreal.log('Spawned HISM with %d instances' % hism_component.get_instance_count())
else:
	unreal.log_error("Error during generation")

unreal.EditorLevelLibrary.set_selected_level_actors(selected_actors)