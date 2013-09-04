# Matthew Alger, 2013


from PIL import Image, ImageDraw, ImageFont

class PointlessWrapperClass(object):
    def __init__(self):
        self.fontSize = 18
        self.fontFile = "./times.ttf"
        self.font = ImageFont.truetype(self.fontFile, self.fontSize)

    def fraction(self, numerator, denominator, colour=(0, 0, 0)):
        # Get the image of the numerator and denominator.
        numeratorImg = numerator[0](*numerator[1:])
        denominatorImg = denominator[0](*denominator[1:])

        # The height will be the height of both children, plus three. Width is max of both.
        thisWidth, thisHeight = boxSize = max(numeratorImg.size[0], denominatorImg.size[0]), numeratorImg.size[1] + 3 + denominatorImg.size[1]

        # Draw the image.
        img = Image.new("RGB", boxSize, (255, 255, 255))
        img.paste(numeratorImg, ((thisWidth - numeratorImg.size[0])//2, 0))
        img.paste(denominatorImg, ((thisWidth - denominatorImg.size[0])//2, numeratorImg.size[1] + 3))
        draw = ImageDraw.Draw(img)
        draw.line((0, numeratorImg.size[1] + 2, thisWidth, numeratorImg.size[1] + 2), fill=colour)

        return img

    def sqrt(self, child, colour=(0, 0, 0)):
        # Get the image that goes inside this sqrt.
        childImg = child[0](*child[1:])

        # Calculate the heights of the sqrt.
        childWidth, childHeight = childImg.size
        thisWidth, thisHeight = boxSize = childWidth + self.fontSize//2 + 1, childHeight + 3

        # Draw the image.
        img = Image.new("RGB", boxSize, (255, 255, 255))
        img.paste(childImg, (self.fontSize//2 + 1, 3))
        draw = ImageDraw.Draw(img)
        draw.line((0, thisHeight-self.fontSize//2, self.fontSize//4, thisHeight-2), fill=colour)
        draw.line((self.fontSize//4, thisHeight-2, self.fontSize//2, 2), fill=colour)
        draw.line((self.fontSize//2, 2, thisWidth, 2), fill=colour)

        return img

    def number(self, n, colour=(0, 0, 0)):
        # Get the size of the literal
        n = str(n)
        boxSize = (self.font.getsize(n)[0], self.fontSize)

        # Write literal to image
        img = Image.new("RGB", boxSize, (255,255,255))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), n, colour, font=self.font)

        return img


if __name__ == '__main__':
    p = PointlessWrapperClass()
    z = p.sqrt(
            (p.fraction,
                (p.fraction,
                    (p.sqrt,
                        (p.number, 10)),
                    (p.number, 10)),
                (p.sqrt,
                    (p.sqrt,
                        (p.number, "a^2 + b^2")))))
    z.save("test.png")
    print(z.size)
