class Color:
    """
    A simple class for displaying a colored dot in the console using ANSI Escape codes.

    Attributes:
        r (int): The red component of the RGB color (0 to 255).
        g (int): The green component of the RGB color (0 to 255).
        b (int): The blue component of the RGB color (0 to 255).
    """

    def __init__(self, r, g, b):
        """
        Initializes a Color object with the specified RGB values.

        Args:
            r (int): The red component of the RGB color (0 to 255).
            g (int): The green component of the RGB color (0 to 255).
            b (int): The blue component of the RGB color (0 to 255).
        """
        self.r = r
        self.g = g
        self.b = b

    def print_colored_dot(self):
        """
        Prints a colored dot in the console using ANSI Escape codes.
        """
        print(f"\033[38;2;{self.r};{self.g};{self.b}m●\033[0m")

    def rgb_to_ansi(self):
        """
        Converts RGB values to ANSI color code.

        Returns:
            int: The ANSI color code.
        """
        ansi_r = int((self.r / 255) * 5)
        ansi_g = int((self.g / 255) * 5)
        ansi_b = int((self.b / 255) * 5)
        ansi_color_code = 16 + (36 * ansi_r) + (6 * ansi_g) + ansi_b
        return ansi_color_code

    def __eq__(self, other):
        """
        Compares two Color objects for equality based on their RGB values.

        Args:
            other (Color): The Color object to compare with.

        Returns:
            bool: True if the colors are equal, False otherwise.
        """
        if isinstance(other, Color):
            return self.r == other.r and self.g == other.g and self.b == other.b
        return False

    def __add__(self, other):
        """
        Adds two Color objects by combining their RGB values.

        Args:
            other (Color): The Color object to add.

        Returns:
            Color: A new Color object representing the result of the addition.
        """
        if isinstance(other, Color):
            new_r = min(self.r + other.r, 255)
            new_g = min(self.g + other.g, 255)
            new_b = min(self.b + other.b, 255)
            return Color(new_r, new_g, new_b)
        else:
            raise TypeError("Unsupported operand type. Use Color objects for addition.")

    def __hash__(self):
        """
        Returns a hash value for the Color object.

        Returns:
            int: The hash value.
        """
        return hash((self.r, self.g, self.b))

    def __mul__(self, c):
        """
        Multiplies the RGB values of the Color object by a scalar factor.

        Args:
            c (float): The scalar factor.

        Returns:
            Color: A new Color object with scaled RGB values.
        """
        new_r = int(self.r * c)
        new_g = int(self.g * c)
        new_b = int(self.b * c)
        return Color(new_r, new_g, new_b)


if __name__ == "__main__":
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)

    red.print_colored_dot()
    green.print_colored_dot()
    blue.print_colored_dot()

    print(red == green)
    print(red == Color(255, 0, 0))

    result_color = red + green
    result_color.print_colored_dot()

    orange1 = Color(255, 165, 0)
    orange2 = Color(255, 165, 0)
    color_list = [orange1, red, green, orange2]

    unique_colors = list(set(color_list))

    for color in unique_colors:
        color.print_colored_dot()

    half_red = red * 0.5
    half_red.print_colored_dot()