# UEPythonTools

##  Instantiate.py

  short
  -----
  If you have lots of static mesh you want to group into a Hierarchical Instancied Static Mesh.
  
  description
  -------
  This tool will group your selection by StaticMesh type, then create a ISM per StaticMesh. 
  Multiple StaticMesh results in multiple InstancedStaticMeshActor
  
  limitations
  -------
  You have to create a small BP in your project. 
  1. New Actor (/Game/BP_InstancedStaticMeshActor)
  2. Add HierarchicalInstancedStaticMeshComponent
  3. Set as Root Component.

  The property system does not work as expected, it is not able to transfer material override or mobility (etc).
  
  args
  ------
	-d	Delete StaticMeshActors after creation
	-p	Define Prototype of the actor type (ex: Blueprint'/Game/BP_InstancedStaticMeshActor.BP_InstancedStaticMeshActor')
	-h	Print help

##  ISMFromSelection.py

  short
  -----
  If you have Actors you wan to replace with Instances, but those are not StaticMeshActors.
  
  description
  -------
  This tool will Add all Transform of your selection into a InstancedStaticMeshComponent. 
  
  limitations
  -------
  You have to create a small BP in your project. 
  1. New Actor (/Game/BP_InstancedStaticMeshActor)
  2. Add HierarchicalInstancedStaticMeshComponent
  3. Set as Root Component.

  args
  ------
	-p	Define Prototype of the actor type (ex: Blueprint'/Game/BP_InstancedStaticMeshActor.BP_InstancedStaticMeshActor')
	-h	Print this help
