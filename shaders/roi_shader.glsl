#vertex
#version 420

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 UV;
out vec2 fUV;

uniform mat4 cameraMatrix;
uniform mat4 modelMatrix;

void main()
{
    gl_Position = cameraMatrix * vec4(position, 1.0);
    fUV = UV;
}

#fragment
#version 420

layout (binding = 0) uniform usampler2D image;

out vec4 fragmentColor;

in vec2 fUV;
uniform vec3 roiColour;
uniform float lineWidth;
uniform float roiWidth;
uniform float roiHeight;

void main()
{
    float wScaleFac = max(1.0, roiWidth / roiHeight);
    float hScaleFac = max(1.0, roiHeight / roiWidth);
    float sharedScaleFac = max(roiWidth, roiHeight);
    vec2 UV = vec2(fUV.x * wScaleFac, fUV.y * hScaleFac);
    float dw = abs(-min(fUV.x, 1.0 - fUV.x) * max(1.0, roiWidth / roiHeight) * sharedScaleFac);
    float dh = abs(-min(fUV.y, 1.0 - fUV.y) * max(1.0, roiHeight / roiWidth) * sharedScaleFac);
    if ((dw < lineWidth) || (dh < lineWidth))
        fragmentColor = vec4(roiColour, 1.0);
    else
        fragmentColor = vec4(0.0, 0.0, 0.0, 0.0);
}