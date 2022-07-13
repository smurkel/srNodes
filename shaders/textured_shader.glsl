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
uniform float contrast_min;
uniform float contrast_max;

void main()
{
    float pixelValue = (float(texture(image, fUV)).r);
    pixelValue -= contrast_min;
    pixelValue /= (contrast_max - contrast_min);
    fragmentColor = vec4(pixelValue, pixelValue, pixelValue, 1.0);
}