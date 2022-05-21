#vertex
#version 420

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 UV;
out vec2 fUV;

uniform mat4 cameraMatrix;

void main()
{
    gl_Position = cameraMatrix * vec4(position.xyz, 1.0);
    fUV = UV;
}

#fragment
#version 420

layout (binding = 0) uniform usampler2D image;

out vec4 fragmentColor;

in vec2 fUV;

void main()
{
    fragmentColor = vec4(fUV, 0.0, 1.0);
}