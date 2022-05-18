## srNodes

srNodes is a node-editor for super-resolution fluorescence microscopy image reconstruction. The goal of this project is to facilitate image reconstruction by providing a single, flexible interface, within which one can link up and explore various image processing steps in order to generate a processing pipeline that is well suited for their particular dataset and/or sample type.

The following common processing steps will be available. They are listed roughly in order of use:
1. Image registration / drift correction
2. Spatial filters
3. Temporal filters
4. Image-content conditional filters
5. Particle detection
6. Particle fitting
7. Particle filtering

   

### Notes during development
#### Node list
- MicroscopeParametersNode
- ReconstructionNode
- RegisterNode
- LoadDataNode

#### Attribute list
- InputTextAttribute
- FileAttribute
- FloatAttribute
- SystemParametersAttribute

