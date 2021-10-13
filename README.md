# UEPythonTools

##  Instantiate.py

  short
  If you have lots of static mesh you want to group into a Hierarchical Instancied Static Mesh.
  
  description
  This tool will group your selection by StaticMesh type. then create a HISM per StaticMesh. 
  
  limitations
  You have to create a small BP in your project. 
    1. New Actor (/Game/BP_InstancedStaticMeshActor)
    2. Add HierarchicalInstancedStaticMeshComponent
    3. Set as Root Component.
  The property system does not work as expected, it is not able to transfer material override or mobility (etc).
  
  args
  ```
    -e  delete selected Static Mesh Actors
  ```
