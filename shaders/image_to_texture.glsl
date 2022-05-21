#vertex
#version 420

layout(location = 0) in vec3 position;
out vec2 UV;


void main()
{
    gl_Position = vec4(position, 1.0);
}

#fragment
#version 420

layout (binding = 0) uniform usampler2D image;

out vec4 fragmentColor;

uniform float image_width;
uniform float image_height;

void main()
{
    vec2 UV = gl_FragCoord.xy / min(image_width, image_height);
    if (image_height > image_width)
    {
        UV.x = UV.x / (image_height / image_width);
    }
    float pixel_value = float(texture(image, UV).r);
    float min = 0.0;
    float max = 1000.0;
    pixel_value = (pixel_value - min) / (max - min);
    fragmentColor = vec4(pixel_value, pixel_value, pixel_value, 1.0);

}