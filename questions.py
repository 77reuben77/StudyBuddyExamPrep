import matplotlib.pyplot as plt
import random
import math
import fractions
from sympy import *
import numpy as np
from matplotlib_venn import venn3
from fractions import Fraction
import textwrap

afrikaans_names = [
    "Anika",
    "Benjamin",
    "Charlize",
    "Danie",
    "Elsje",
    "Francois",
    "Gerhard",
    "Helena",
    "Izak",
    "Jan",
    "Karin",
    "Lize",
    "Marius",
    "Nadia",
    "Oscar",
    "Petra",
    "Quintin",
    "Riaan",
    "Stefan",
    "Tiaan",
    "Ulrich",
    "Vivian",
    "Willem",
    "Xander",
    "Yolanda",
    "Zelda",
    "Andries",
    "Bianca",
    "Christiaan",
    "Dina",
    "Ernst",
    "Frederika",
    "Gideon",
    "Hendrik",
    "Ilse",
    "Johan",
    "Katrina",
    "Lukas",
    "Magda",
    "Nico",
    "Olivia",
    "Pieter",
    "Quinta",
    "Renate",
    "Suzanne",
    "Theo",
    "Ursula",
    "Vincent",
    "Wynand",
    "Xenia",
    "Yvette",
    "Zander"
]


################################################################


def generate_picture(latex_text, annotation):
    fig = plt.figure(figsize=(6, 3))

    # Remove all axes for a blank figure
    plt.axis('off')

    # Add the LaTeX equation to the figure, enclosed in dollar signs
    if latex_text != "":
        plt.text(0.5, 0.3, f"${latex_text}$", size=24, ha='center')  # reduced y-coordinate from 0.5 to 0.4
    # Add annotation
    plt.text(0.5, 0.6, annotation, size=14, ha='center')  # increased y-coordinate from 0.5 to 0.6

    # Generate a unique filename using the current timestamp and a random UUID
    filename = f"/tmp/output.png"

    # Save the figure as an image
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)

    # Close the figure
    plt.close(fig)


################################################################
# Algebra functions

def _random_non_zero(lower, upper):
    # generates a random number between the lower and upper bounds but excludes zero as an option
    x = random.randint(lower, upper)
    while x == 0:
        x = random.randint(lower, upper)

    return x


def _prettify_number(num, is_c=False):
    # Formats the number to a string which is usable in an equation
    # is_c is a boolean value for if a number stands alone and is not merely a quotient of a variable
    if num == 1 and is_c:
        num_string = "+ 1"
    elif num == 1:
        num_string = "+ "
    elif num == -1 and is_c:
        num_string = "- 1"
    elif num == -1:
        num_string = "- "
    elif num < 0:
        num_string = f"- {num.__abs__()}"
    else:
        num_string = f"+ {num}"

    return num_string


def _scramble(a, b, c):
    # This function takes a quadratic equation in the form ax^2 + bx + c = 0
    # It then shifts one of the variables to the other side of the equation and returns the scrambled equation
    scrambled = random.choice([True, False])

    if not scrambled:
        equation = f"{_prettify_number(a)}x^2 {_prettify_number(b)}x {_prettify_number(c, True)} = 0".strip("+")
    else:
        scramble = random.choice([1, 2, 3])
        if scramble == 1:
            p1 = f"{_prettify_number(b)}x {_prettify_number(c, True)}".strip("+")
            p2 = f"{_prettify_number(-a)}x^2 ".strip("+")
            equation = f"{p1} = {p2}"
        elif scramble == 2:
            p1 = f"{_prettify_number(a)}x^2 {_prettify_number(c, True)}".strip("+")
            p2 = f"{_prettify_number(-b)}x ".strip("+")
            equation = f"{p1} = {p2}"
        else:
            p1 = f"{_prettify_number(a)}x^2 {_prettify_number(b)}x".strip("+")
            p2 = f"{_prettify_number(-c, True)} ".strip("+")
            equation = f"{p1} = {p2}"

    return equation


def _gen_factored_quadratic(provide_ijkl=False):
    # generates a quadratic expression that has the potential to be factored
    i = _random_non_zero(-5, 5)
    j = _random_non_zero(-5, 5)
    k = _random_non_zero(-5, 5)
    l = _random_non_zero(-5, 5)

    a = i * k
    c = -j * (-l)
    b = i * (-l) + k * (-j)

    r1 = fractions.Fraction(j, i)
    r2 = fractions.Fraction(l, k)

    if provide_ijkl:
        return a, b, c, r1, r2, i, j, k, l
    else:
        return a, b, c, r1, r2


def _gen_unfactored_quadratic():
    # generates a random quadratic expression
    a = _random_non_zero(-10, 10)
    b = _random_non_zero(-10, 10)
    c = _random_non_zero(-10, 10)

    try:
        r1 = (-b + math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
        r2 = (-b - math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    except ValueError:
        # This will be executed when b^2 - 4ac is negative
        r1 = None
        r2 = None
        print("The equation has complex roots.")

    return a, b, c, r1, r2


def _solve_quadratic_inequality(a, r1, r2, i_sign):
    # determines the solutions to a quadratic inequality
    if r1 > r2:
        placeholder = r1
        r1 = r2
        r2 = placeholder

    if r1 == r2 and (i_sign == "<" or i_sign == ">"):
        solution = "Geen oplossing"

    elif i_sign == "<" or i_sign == "\\leq":
        if a > 0:
            solution = f"{r1} < x < {r2}; x \\in reeële getalle"
        else:
            solution = f"x < {r1} of x > {r2}; x \\in reeële getalle"
        if i_sign == "\\leq":
            solution = solution.replace("<", "\\leq")
            solution = solution.replace(">", "\\geq")

    else:
        if a > 0:
            solution = f"x < {r1} of x > {r2}; x \\in reeële getalle"
        else:
            solution = f"{r1} < x < {r2}; x \\in reeële getalle"
        if sign == "\\geq":
            solution = solution.replace("<", "\\leq")
            solution = solution.replace(">", "\\geq")

    return solution


class Algebra:

    def __init__(self, current_sub_topic):

        algebra_handlers = {
            'factored_quadratic_problem': self.factored_quadratic_problem,
            'unfactored_quadratic_problem': self.unfactored_quadratic_problem,
            'quadratic_inequality_problem': self.quadratic_inequality_problem,
            'rooted_quadratic_problem': self.rooted_quadratic_problem,
            'simultaneous_equation_problem': self.simultaneous_equation_problem
        }

        handler = algebra_handlers.get(current_sub_topic)
        if handler:
            self.problem, self.solution = handler()
        else:
            print(f"Warning: Unhandled state '{current_sub_topic}'")

    def get_problem_and_solution(self):
        return self.problem, self.solution

    @staticmethod
    def factored_quadratic_problem():
        # generates in the form (ix-j)(kx-l)= 0
        # but returns a problem in the form ax^2 + bx + c = 0
        a, b, c, r1, r2, i, j, k, l = _gen_factored_quadratic(provide_ijkl=True)

        equation = _scramble(a, b, c)

        annotation = "Los die volgende kwadratiese vergelyking op:"
        generate_picture(equation, annotation)

        problem = annotation + "\n" + equation
        solution = \
            f"Metode 1: Faktorisering" \
            f"\n1. Kry in die vorm $ax^2 + bx + c = 0$" \
            f"\n   ${a}x^2 {_prettify_number(b)}x {_prettify_number(c, True)} = 0$" \
            f"\n2. Faktoriseer die drieterm" \
            f"\n   $({i}x {_prettify_number(-j, True)})({k}x {_prettify_number(-l, True)}) = 0$" \
            f"\n3. Stel elke hakie gelyk aan 0 aangesien enige iets maal 0 is 0:" \
            f"\n   $({i}x {_prettify_number(-j, True)}) = 0$ of $({k}x {_prettify_number(-l, True)}) = 0$" \
            f"\n4. Los op om die wortels te kry:" \
            f"\n   $x = \\frac{{{j}}}{{{i}}}$  of  $x = \\frac{{{l}}}{{{k}}}$" \
            f"\n" \
            f"\nMetode 2: Kwadratiese formule:" \
            f"\n" \
            f"\n5. Finale Antwoord:" \
            f"\n $x = {r1}$ of $x = {r2}$ (Altwee moet genoem word)"

        return problem, solution

    @staticmethod
    def unfactored_quadratic_problem():
        a, b, c, r1, r2 = _gen_unfactored_quadratic()

        equation = _scramble(a, b, c)
        annotation = "Los die volgende kwadratiese vergelyking op:"

        generate_picture(equation, annotation)

        problem = f"{annotation} \n{equation}"
        if r1 is None and r2 is None:
            solution = f"Gebruik die kwadratiese formule: $x = \\frac{{-b \\pm \\sqrt{{b^2-4ac}}}}{{2a}}$" \
                       f"\na = {a}, b = {b}, c = {c}" \
                       f"\nPlaas die waardes van a, b, en c in: $x = \\frac{{-{b} \\pm \\sqrt{{{b}^2-4({a})({c})}}}}{{2({a})}}$" \
                       f"\nFinale antwoord:" \
                       f"\nd.w.s. x het geen (reeele) oplossing nie."
        else:
            solution = f"Gebruik die kwadratiese formule: $x = \\frac{{-b \\pm \\sqrt{{b^2-4ac}}}}{{2a}}$" \
                       f"\na = {a}, b = {b}, c = {c}" \
                       f"\nPlaas die waardes van a, b, en c in: $x = \\frac{{-{b} \\pm \\sqrt{{{b}^2-4({a})({c})}}}}{{2({a})}}$" \
                       f"\nFinale antwoord:" \
                       f"\nx = {r1} of x = {r2}"

        return problem, solution

    @staticmethod
    def quadratic_inequality_problem():
        a, b, c, r1, r2 = _gen_factored_quadratic()
        equation = _scramble(a, b, c)
        operand_choice = random.choice([[1, "<"], [2, ">"], [3, "\\leq"], [4, "\\geq"]])
        inequality = equation.replace("=", operand_choice[1])
        annotation = "Los die volgende ongelykheid op:"

        problem = f"{annotation}\n{inequality}"

        if a > 0:
            solution = \
                f"Begin deur die kritieke waardes te kry:" \
                f"\nkw1 = {r1}, kw2 = {r2}" \
                f"\nKyk waar die uitdrukking positief of negatief sal wees:" \
                f"\nOmdat a positief is, is die uitrudding negatief tussen in die kritieke waardes." \
                f"Finale antwoord: \n\n${_solve_quadratic_inequality(a, r1, r2, operand_choice[1])}$"
        else:
            solution = \
                f"Begin deur die kritieke waardes te kry:" \
                f"\nkw1 = {r1}, kw2 = {r2}" \
                f"\nKyk waar die uitdrukking positief of negatief sal wees:" \
                f"\nOmdat a negatief is, is die uitrudding positief tussen in die kritieke waardes." \
                f"Finale antwoord: \n\n${_solve_quadratic_inequality(a, r1, r2, operand_choice[1])}$"
        generate_picture(inequality, annotation)

        return problem, solution

    @staticmethod
    def rooted_quadratic_problem():
        # this function takes a normal quadratic equation and converts it anto a 'square rooted' 3-term problem
        a, b, c, r1, r2 = _gen_factored_quadratic()
        r1 = (r1.numerator / r1.denominator) * (r1.numerator / r1.denominator)
        r2 = (r2.numerator / r2.denominator) * (r2.numerator / r2.denominator)

        equation = _scramble(a, b, c).replace("x^2", "y").replace("x", "\\sqrt{x}").replace("y", "x")
        annotation = "Los die volgende vergelyking op:"

        generate_picture(equation, annotation)
        problem = f"{annotation} \n{equation}"
        solution = f"Gebruik die kwadratiese formule: $x = \\frac{{-b \\pm \\sqrt{{b^2-4ac}}}}{{2a}}$" \
                   f"\na = {a}, b = {b}, c = {c}" \
                   f"\nPlaas die waardes van a, b, en c in: $\\sqrt{{x}} = \\frac{{-{b} \\pm \\sqrt{{{b}^2-4({a})({c})}}}}{{2({a})}}$" \
                   f"\n$x = (\\frac{{-{b} \\pm \\sqrt{{{b}^2-4({a})({c})}}}}{{2({a})}})^2$" \
                   f"\nFinale antwoord:" \
                   f"\nx = {r1} of x = {r2}"

        return problem, solution

    @staticmethod
    def simultaneous_equation_problem():
        x = _random_non_zero(-10, 10)
        y = _random_non_zero(-10, 10)
        a1 = _random_non_zero(-10, 10)
        b1 = _random_non_zero(-10, 10)
        c1 = a1 * x + b1 * y

        equation1 = f"{_prettify_number(a1)}x {_prettify_number(b1)}y = {_prettify_number(c1, True)}".strip("+")

        a2 = _random_non_zero(-10, 10)
        b2 = _random_non_zero(-10, 10)

        e_type = random.choice([1, 2, 3])
        if e_type == 1:
            c = (a2 * x * x) + (b2 * y)
            equation2 = f"{_prettify_number(a2)}x^2 {_prettify_number(b2)}y = {_prettify_number(c)}".strip("+")
            a3 = a2
            b3 = -(a1 * b2) / b1
            c3 = (b2 * c1) / b1 - c
            x1 = (-b3 + (sqrt((b3 * b3) - (4 * a3 * c3)))) / (2 * a3)
            x2 = (-b3 - (sqrt((b3 * b3) - (4 * a3 * c3)))) / (2 * a3)
            y1 = (c1 - (a1 * x1)) / b1
            y2 = (c1 - (a1 * x2)) / b1
        elif e_type == 2:
            c = (a2 * x) + (b2 * y * y)
            equation2 = f"{_prettify_number(a2)}y^2 {_prettify_number(b2)}x = {_prettify_number(c)}".strip("+")
            a3 = a2
            b3 = -(b2 * b1) / a1
            c3 = ((b2 * c1) / a1) - c
            y1 = (-b3 + (sqrt((b3 * b3) - (4 * a3 * c3)))) / (2 * a3)
            y2 = (-b3 - (sqrt((b3 * b3) - (4 * a3 * c3)))) / (2 * a3)
            x1 = (c1 - (b1 * y1)) / a1
            x2 = (c1 - (b1 * y2)) / a1
        else:
            c = (a2 * x * y) + (b2 * y)
            equation2 = f"{_prettify_number(a2)}xy {_prettify_number(b2)}y = {_prettify_number(c)}".strip("+")
            a3 = (-b1 * a2) / a1
            b3 = ((a2 * c1) / a1) + b2
            c3 = -c
            y1 = (-b3 + (sqrt((b3 * b3) - (4 * a3 * c3)))) / (2 * a3)
            y2 = (-b3 - (sqrt((b3 * b3) - (4 * a3 * c3)))) / (2 * a3)
            x1 = (c1 - (b1 * y1)) / a1
            x2 = (c1 - (b1 * y2)) / a1

        latex_text = f"{equation1} ; {equation2}"
        annotation = "Rond af tot 2 desimale as dit nodig is vir die volgende vraag.\n\nLos gelyktydig op vir x en y."

        generate_picture(latex_text, annotation)

        problem = f"{annotation}\n{latex_text}"
        solution = f"x = {x} en y = {y}"
        solution1 = f"x1 = {x1} en y1 = {y1}"
        solution2 = f"x2 = {x2} en y2 = {y2}"

        return problem, solution


############################################################
# Calculus

class Calculus:
    problem = ""
    solution = ""

    def __init__(self, current_sub_topic):
        calculus_handlers = {
            'first_principles_problem': self.first_principles_problem,
            'derivative_problem': self.derivative_problem,
            'minimum_gradient_problem': self.minimum_gradient_problem,
        }

        handler = calculus_handlers.get(current_sub_topic)
        if handler:
            self.problem, self.solution = handler()
        else:
            print(f"Warning: Unhandled state '{current_sub_topic}'")

    def get_problem_and_solution(self):
        return self.problem, self.solution

    @staticmethod
    def first_principles_problem():
        a, b, c, r1, r2 = _gen_unfactored_quadratic()
        fx = f"{_prettify_number(a)}x^2 {_prettify_number(b)}x {_prettify_number(c, True)}".strip("+")
        latex = f"f(x) = {fx}"
        annotation = "Bepaal f'(x) van eerste beginsels:"
        generate_picture(latex, annotation)

        problem = f"{annotation}\n{latex}"
        solution = f"\n$f'(x) = \\lim_{{h \\to 0}} \\frac{{f(x+h)-f(x)}}{{h}}$" \
                   f"\n$f'(x) = \\lim_{{h \\to 0}} \\frac{{({_prettify_number(a)}(x+h)^2 {_prettify_number(b)}(x+h) " \
                   f"{_prettify_number(c, True)}) - ({fx})}}{{h}}$" \
                   f"\n$f'(x) = \\lim_{{h \\to 0}} \\frac{{{a}x^2 + {2 * a}xh + {a}h^2 + {b}x + {b}h + c - ({fx})}}{{h}}$" \
                   f"\n$f'(x) = \\lim_{{h \\to 0}} \\frac{{{a}x^2 - {a}x^2 + {b}x - {b}x + {c} - {c} +{2 * a}xh + {a}h^2 + {b}h}}{{h}}$" \
                   f"\n$f'(x) = \\lim_{{h \\to 0}} \\frac{{{2 * a}xh + {a}h^2 + {b}h}}{{h}}$" \
                   f"\n$f'(x) = \\lim_{{h \\to 0}} ({2 * a}x + {a}h + {b})\\frac{{h}}{{h}}$" \
                   f"\n$f'(x) = {2 * a}x + {a}(0) + {b}$" \
                   f"\n$f'(x) = {2 * a}x + {b}$"

        return problem, solution

    @staticmethod
    def derivative_problem():
        degree1 = random.randint(1, 8)
        degree2 = random.randint(1, 8)
        while degree1 == degree2:
            degree2 = random.randint(1, 8)
        degree3 = random.randint(1, 8)
        while degree3 == degree2 or degree3 == degree1:
            degree3 = random.randint(1, 8)

        a, b, c, r1, r2 = _gen_unfactored_quadratic()
        fx = f"{_prettify_number(a)}x^{degree1} {_prettify_number(b)}x^{degree2}" \
             f" {_prettify_number(c)}x^{degree3}".strip("+").replace("^1", "")

        latex = f"f(x) = {fx}"
        annotation = "Bepaal f'(x) as:"
        generate_picture(latex, annotation)

        problem = f"{annotation}\n{latex}"
        solution = f"{_prettify_number(a * degree1)}x^{{{(degree1 - 1)}}} {_prettify_number(b * degree2)}x^{{{(degree2 - 1)}}} " \
                   f"{_prettify_number(c * degree3)}x^{{{(degree3 - 1)}}}".strip("+").replace("^1", "").replace(" x^0",
                                                                                                                "1").replace(
            "x^0", "")
        solution = f"\nMaal die magte van x met die onderskeie koeffisiente." \
                   f"\nDan minus een van die onderskeie magte (van x)." \
                   f"\n\n$f'(x) = {solution}$"

        print(solution)
        return problem, solution

    @staticmethod
    def minimum_gradient_problem():
        # a = random.randint(1, 10)
        b = random.randint(1, 10)
        b2 = b * 2
        c = random.randint(1, 10)
        d = random.randint(1, 10)
        tpx = _random_non_zero(-10, 10)
        a2 = (tpx * (-b2)) / 2
        a = -b2 / (tpx * 6)
        tpy = a2 * (tpx ** 2) + b2 * tpx + c

        fx = f"ax^3 {_prettify_number(b)}x^2 + cx + d".strip("+")
        latex = f"g(x) = {fx}"

        up_or_down = random.choice(["op", "af"])
        annotation = f"Die raaklyn op g(x) het 'n minimum helling by die punt \n" \
                     f"({tpx}; {tpy}). Vir watse waardes van x is g(x) konkaaf {up_or_down}?"

        generate_picture(latex, annotation)

        problem = f"{annotation}\n{latex}"
        if up_or_down == "up":
            solution = f"Begin deur $g'(x)$ en $g''(x)$ te bereken\n" \
                       f"\n$g'(x) = 3ax^2 {_prettify_number(b2)}x + c$" \
                       f"\n$g''(x) = 6ax {_prettify_number(b2, True)}$" \
                       f"\nStel $g''(x) = 0$ by $x = {tpx}$ en los op vir $a$" \
                       f"\n$6a{tpx} {_prettify_number(b2, True)} = 0$" \
                       f"\n$a = \\frac{{{-b2}}}{{{tpx * 6}}}$" \
                       f"\n$a = {-b2 / (tpx * 6)}$" \
                       f"\nOm die waardes van $x$ te vind waar konkawiteit opwaarts is, stel $g''(x)>0$" \
                       f"\n$6({a})x {_prettify_number(b2, True)} > 0$" \
                       f"\n$x > \\frac{{{-b2}}}{{6({a})}}$" \
                       f"\n$x > \\frac{{{-b2}}}{{{6 * a}}}$" \
                       f"\n$x > {(-b2 / (6 * a)).__round__(4)}$"


        else:
            solution = f"Begin deur $g'(x)$ en $g''(x)$ te bereken\n" \
                       f"\n$g'(x) = 3ax^2 {_prettify_number(b2)}x + c$" \
                       f"\n$g''(x) = 6ax {_prettify_number(b2, True)}$" \
                       f"\nStel $g''(x) = 0$ by $x = {tpx}$ en los op vir $a$" \
                       f"\n$6a{tpx} {_prettify_number(b2, True)} = 0$" \
                       f"\n$a = \\frac{{{-b2}}}{{{tpx * 6}}}$" \
                       f"\n$a = {-b2 / (tpx * 6)}$" \
                       f"\nOm die waardes van $x$ te vind waar konkawiteit afwaarts is, stel $g''(x) < 0$" \
                       f"\n$6({a})x {_prettify_number(b2, True)} < 0$" \
                       f"\n$x < \\frac{{{-b2}}}{{6({a})}}$" \
                       f"\n$x < \\frac{{{-b2}}}{{{6 * a}}}$" \
                       f"\n$x < {(-b2 / (6 * a)).__round__(4)}$"

        return problem, solution


############################################################
# Finance


def _compound_interest():
    p = _random_non_zero(1, 15) * 1000
    i = _random_non_zero(5, 12) / 100
    n = _random_non_zero(2, 20)
    comp_timeframe = random.choice([[1, 'jaarliks'], [2, 'twee-jaarliks'], [4, 'kwartaalliks'], [12, 'maandeliks']])
    # each number represents a different compounded rate.
    # 1 = yearly
    # 2 = bi-annually
    # 4 = quarterly
    # 12 = monthly
    a = p * (1 + i / comp_timeframe[0]) ** (n * comp_timeframe[0])

    return p, i, n, a, comp_timeframe


def _convert_interest_rate(i, comp_timeframe, new_time_frame):
    i2 = (((1 + i / comp_timeframe[0]) ** comp_timeframe[0]) ** (1 / new_time_frame[0]) - 1) * new_time_frame[0]
    return i2


def _annuity(is_future=True):
    x = random.randint(1, 12) * 1000
    i = _random_non_zero(5, 12) / 100
    n = _random_non_zero(2, 20)
    comp_timeframe = random.choice([[1, 'yearly'], [2, 'bi-annually'], [4, 'quarterly'], [12, 'monthly']])
    # each number represents a different compounded rate.
    # 1 = yearly
    # 2 = bi-annually
    # 4 = quarterly
    # 12 = monthly

    f = x * (((1 + i / comp_timeframe[0]) ** (n * comp_timeframe[0])) - 1) / (i / comp_timeframe[0])

    return x, i, n, f, comp_timeframe


class Finance:
    problem = ""
    solution = ""

    def __init__(self, current_sub_topic):
        finance_handlers = {
            'unknown_interest_problem': self.unknown_interest_problem,
            'annuity_will_he_make_it_problem': self.annuity_will_he_make_it_problem,
            'delayed_car_payment_loan': self.delayed_car_payment_loan
        }
        handler = finance_handlers.get(current_sub_topic)
        if handler:
            self.problem, self.solution = handler()
        else:
            print(f"Warning: Unhandled state '{current_sub_topic}'")

    def get_problem_and_solution(self):
        return self.problem, self.solution

    @staticmethod
    def unknown_interest_problem():
        p, i, n, a, comp_timeframe = _compound_interest()

        problem = f"\nR{p.__round__()} was belê in 'n beleggingsfonds wat rente uitbetaal teen \n" \
                  f"m% per jaar, {comp_timeframe[1]} saamgestel. Na {n} jare, \n" \
                  f"was die waarde van die belegging R{a.__round__(2)}\n\n Bereken " \
                  f"die rentekoers, m."
        generate_picture("", problem)

        solution = f"Begin deur 'n samegestelde rente formule op te stel: " \
                   f"$a = p\\left(1+\\frac{{m}}{{ {comp_timeframe[0]} }}\\right)^{{n \\times {comp_timeframe[0]}}}$\n" \
                   f"Vervang alle bekende waardes in: " \
                   f"${a.__round__()} = {p}\\left(1+\\frac{{m}}{{ {comp_timeframe[0]} }}\\right)^{{ {n} \\times {comp_timeframe[0]} }}$\n" \
                   f"Los op vir m: " \
                   f"$m = \\left(\\sqrt[{n} \\times {comp_timeframe[0]}]{{\\frac{{{a.__round__()}}}{{{p}}}}} - 1\\right) \\times {comp_timeframe[0]}$\n" \
                   f"\n$m = {i * 100}\\%$"

        return problem, solution

    @staticmethod
    def annuity_will_he_make_it_problem():
        x, i, n, f, comp_timeframe = _annuity()
        item_price = random.randint(f.__round__() - 400, f.__round__() - 400)

        name = random.choice(afrikaans_names)

        problem = f"\n{name} spaar om 'n ring vir sy meisie te koop." \
                  f"Hy maak {comp_timeframe[1]} betalings van R{x} in 'n rekening," \
                  f"vir {n} jare. Die rekening verdien rente teen " \
                  f"{i * 100}% {comp_timeframe[1]} saamgestel." \
                  f"Die ring wat hy wil koop kos R{item_price}." \
                  f"Sal Jaco na {n} jare genoeg geld hê om die ring te koop?"
        problem = textwrap.fill(problem, width=50, break_long_words=False)

        generate_picture("", problem)

        if f > item_price:
            does_or_does_not = ""
        else:
            does_or_does_not = "nie"

        solution = f"Begin deur 'n toekomstige waarde formule op te stel: " \
                   f"\n$F = x \\times \\left(\\frac{{\\left(1+\\frac{{i}}{{ {comp_timeframe[0]} }}\\right)^{{n \\times {comp_timeframe[0]}}} - 1}}{{\\frac{{{i}}}{{ {comp_timeframe[0]}}}}}\\right)$" \
                   f"\nVervang alle bekende waardes in: $F = {x} \\times \\left(\\frac{{\\left(1+\\frac{{ {i} }}{{ {comp_timeframe[0]} }}\\right)^{{ {n} \\times {comp_timeframe[0]} }} - 1}}{{\\frac{{ {i} }}{{ {comp_timeframe[0]}}}}}\\right)$" \
                   f"\nBereken $F = R{f.__round__(4)}$ \nVergelyk dit met die item prys van $R{item_price}$\n" \
                   f"Gevolglik het hy {does_or_does_not} genoeg geld om die ring te koop {does_or_does_not}. "

        return problem, solution

    @staticmethod
    def delayed_car_payment_loan():
        car_price = random.randint(25, 45) * 10000
        deposit_percentage = random.randint(5, 25) / 100
        p = car_price * (1 - deposit_percentage)
        i = _random_non_zero(5, 12) / 100
        n = _random_non_zero(2, 20)
        comp_timeframe = [12, 'monthly']
        months_delayed = random.randint(3, 8)
        loan_at_repayment_start = p * ((1 + i / 12) ** months_delayed)
        x = loan_at_repayment_start / ((1 - (1 + i / 12) ** (-12 * n + months_delayed)) / (i / 12))

        name = random.choice(afrikaans_names)
        problem = f"\n{name} beplan om 'n kar te koop. Die kar kos R{car_price}." \
                  f"Sy gaan 'n {(deposit_percentage * 100).__round__()}% deposito betaal" \
                  f" en 'n lening aangaan vir die balans. Die rente op die lening is " \
                  f"{(i * 100).__round__()}% per jaar, maandeliks saamgestel." \
                  f"\n\nBereken die waarde van die lening en die maandelikse paaiement wat" \
                  f" sy sal moet betaal as die eerste paaiement {months_delayed} maande" \
                  f"plaasvind na die lening aangegaan is. Die lening sal oor 'n tydperk van {n}" \
                  f" jare terugbetaal word nadat dit toegeken is."
        problem = textwrap.fill(problem, width=50, break_long_words=False).replace("maandeliks saamgestel.",
                                                                                   "maandeliks saamgestel.\n\n")
        problem = f"\n{problem}"

        generate_picture("", problem)

        deposit = car_price * deposit_percentage
        solution = \
            f"Eerstens bereken die deposito: $R{car_price} \\times {deposit_percentage} = R{deposit}$\n" \
            f"Verminder dit van die motor prys om die leningswaarde te kry: \n$R{car_price} - R{deposit} = R{car_price - deposit}$\n" \
            f"Bereken die rente wat opeenhop in die maande voor betaling: \n$R{p} \\times \\left(1+\\frac{{{i}}}{{12}}\\right)^{{{months_delayed}}} = R{loan_at_repayment_start.__round__(4)}$\n" \
            f"Stel 'n teenwoordige waarde formule op en los vir x:\n" \
            f" $p = x \\times \\frac{{1-\\left(1+\\frac{{{i}}}{{12}}\\right)^{{-12n}}}}{{{i}/12}}$\n" \
            f" $ {loan_at_repayment_start.__round__(4)} = x \\times \\frac{{1-\\left(1+\\frac{{{i}}}{{12}}\\right)^{{-(12 \\times {n}-{months_delayed})}}}}{{{i}/12}}$\n" \
            f" $x = \\frac{{ {loan_at_repayment_start.__round__(4)} }}{{\\frac{{1-\\left(1+\\frac{{{i}}}{{12}}\\right)^{{-(12 \\times {n}-{months_delayed})}}}}{{{i}/12}}}}$\n" \
            f" $x = R{x.__round__(2)}$"

        return problem, solution

############################################################
# Functions


def _plot_log_graph(base):
    x = np.linspace(0.1, 10, 400)  # Generating x values from 0.1 to 10
    y = np.log(x) / np.log(base)  # Calculating the logarithm with the specified base

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f'Log (base {base})')
    plt.title(f'Logarithmic Graph (Base {base})')
    plt.xlabel('x')
    plt.ylabel('Log(x)')

    fig, ax = plt.subplots()

    ax.plot(x, y)

    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    plt.tight_layout()

    plt.legend()
    fig.savefig('/tmp/output.png', format='png')
    plt.close(fig)


def _plot_hyperbola(p, q, question):
    # Create an array of x values. We'll exclude -p to avoid division by zero.
    x = np.linspace(-p - 10, -p + 10, 400)
    x = x[x != -p]  # Remove -p from x values

    # Compute h(x) values
    h = 1 / (x + p) + q

    # Create a new figure and axis
    fig, ax = plt.subplots()

    # Plot the hyperbola
    ax.plot(x, h)

    # Plot the asymptotes
    ax.axvline(x=-p, color='red', linestyle='--', label=f'x = {-p}')
    ax.axhline(y=q, color='green', linestyle='--', label=f'y = {q}')

    # Setting axes to their origin
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Set the x and y-axis limits
    ax.set_xlim([-p - 10, -p + 10])
    ax.set_ylim([q - 10, q + 10])

    # Set the title of the graph to the "question" content
    ax.set_title(question)

    # Display the legend
    ax.legend()

    # Save the figure as a PNG file
    plt.tight_layout()
    fig.savefig('/tmp/output.png', format='png')
    plt.close(fig)  # Close the plot


def _plot_exponential_and_parabola(a_exp, b, q, a_parab, b_parab, c, question, add_c=False, add_d=False):
    # Create an array of x values
    tp = -b_parab / (2 * a_parab)
    tpy = (a_parab * (tp ** 2)) + (b_parab * tp) + c
    x = np.linspace(tp - 10, tp + 10, 400)

    # Compute g(x) values for the exponential function
    g = a_exp * b ** x + q

    # Compute f(x) values for the parabola
    f = a_parab * x ** 2 + b_parab * x + c

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the exponential graph
    ax.plot(x, g, label=f'g(x)')

    # Plot the parabola
    ax.plot(x, f, label=f'f(x)', linestyle='--')

    # Setting axes to their origin
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Remove values around axes
    ax.set_xticks([])
    ax.set_yticks([])

    # Label x and y axes
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    if add_c:
        # Label the y-intercept of f as 'C'
        ax.text(0.2, c, 'C', fontsize=10, verticalalignment='bottom')
    if add_d:
        ax.text(tp, tpy + 0.2, 'D', fontsize=10, verticalalignment='bottom')

    # Set the x and y-axis limits
    ax.set_xlim([tp - 10, tp + 10])
    ax.set_ylim([tpy - 10, tpy + 10])

    # Set the title of the graph to the "question" content
    ax.set_title(question)

    # Display the legend
    ax.legend()

    plt.tight_layout()
    # Save the figure as a PNG file
    fig.savefig('/tmp/output.png', format='png')
    plt.close(fig)  # Close the plot


def _plot_linear_and_inverse(m, c, question):
    # Create an array of x values
    x = np.linspace(-10, 10, 400)

    # Compute f(x) values for the linear function
    f = m * x + c

    # Compute inverse f^-1(x) values
    f_inv = (x - c) / m

    # Create a new figure and axis
    fig, ax = plt.subplots()

    # Plot the linear graph
    ax.plot(x, f, label=f'f(x) = {m}x + {c}')

    # Plot the inverse graph
    ax.plot(x, f_inv, label=f'f\u207B\u00B9(x)', linestyle='--')

    # Setting axes to their origin
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Remove values around axes
    ax.set_xticks([])
    ax.set_yticks([])

    # Label x and y axes
    ax.set_xlabel('                                                 x')
    ax.set_ylabel('                                                 y')

    ax.set_xlim([-8, 8])
    ax.set_ylim([-8, 8])
    # Set the title of the graph to the "question" content
    ax.set_title(question)

    intersection_x = (-c - c * m) / (m ** 2 - 1)

    ax.text(0, 0, '0', fontsize=10, verticalalignment='bottom')
    ax.text(-0.5, c, 'B', fontsize=10, verticalalignment='bottom')
    ax.text(-c / m, 0, 'D', fontsize=10, verticalalignment='bottom')
    ax.text((c / m) / (1 / m), 0.2, 'C', fontsize=10, verticalalignment='bottom')
    ax.text(intersection_x, m * intersection_x + c, 'A', fontsize=10, verticalalignment='bottom')
    # Display the legend
    ax.legend()

    plt.tight_layout()
    # Save the figure as a PNG file
    fig.savefig('/tmp/output.png', format='png')
    plt.close(fig)  # Close the plot


def _plot_single_parabola(a, b, c, r1, r2, question):
    # Create an array of x values
    tp = -b / (2 * a)
    tpy = (a * (tp ** 2)) + (b * tp) + c
    x = np.linspace(tp - 10, tp + 10, 400)

    y1 = tpy
    y2 = c

    if y1 > y2:
        placeholder = y1
        y1 = y2
        y2 = placeholder

    if r1 > r2:
        placeholder = r1
        r1 = r2
        r2 = placeholder

    # Compute f(x) values for the parabola
    f = a * x ** 2 + b * x + c

    # Create a new figure and axis
    fig, ax = plt.subplots()

    # Plot the parabola
    ax.plot(x, f, label=f"f'(x)")

    # Setting axes to their origin
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.set_xlim([float(r1) - 1, float(r2) + 1])
    ax.set_ylim([y1 - 1, y2 + 1])

    # Remove values around axes
    ax.set_xticks([])
    ax.set_yticks([])

    # Set the title of the graph to the "question" content
    ax.set_title(question)

    ax.text(r1, 0, f'P({r1}; 0)', fontsize=10, verticalalignment='bottom')
    ax.text(r2, 0, f'Q({r2}; 0)', fontsize=10, verticalalignment='bottom')
    ax.text(0, c, f'R(0; {c})', fontsize=10, verticalalignment='bottom')

    # Display the legend
    ax.legend()

    plt.tight_layout()
    # Save the figure as a PNG file
    fig.savefig('/tmp/output.png', format='png')
    plt.close(fig)  # Close the plot


def _gen_connected_parabola_and_exponential_graph():
    a_par = _random_non_zero(-2, 2)
    b_par = _random_non_zero(-5, 10)
    c = _random_non_zero(-10, 10)

    q = c
    if a_par > 0:
        a_exp = -1
    else:
        a_exp = 1

    tpx = -b_par / (2 * a_par)
    tpy = a_par * (tpx ** 2) + b_par * (tpx) + c

    b_exp = ((tpy - q) / a_exp) ** (1 / tpx)

    return a_par, b_par, c, a_exp, b_exp, q


class Functions:

    def __init__(self, current_sub_topic):

        functions_handlers = {
            'hyperbola_unknown_p_and_q_problem': self.hyperbola_unknown_p_and_q_problem,
            'hyperbola_x_intercept_problem': self.hyperbola_x_intercept_problem,
            'new_parabola_from_old_problem': self.new_parabola_from_old_problem,
            'hyperbola_axis_of_symmetry_problem': self.hyperbola_axis_of_symmetry_problem,
            'hyperbola_inequality_question': self.hyperbola_inequality_question,
            'para_expo_c_problem': self.para_expo_c_problem,
            'para_expo_d_problem': self.para_expo_d_problem,
            'para_expo_b_and_q_problem': self.para_expo_b_and_q_problem,
            'para_expo_g_range_problem': self.para_expo_g_range_problem,
            'adding_k_to_f_problem': self.adding_k_to_f_problem,
            'linear_inverse_c_problem': self.linear_inverse_c_problem,
            'linear_inverse_equation_problem': self.linear_inverse_equation_problem,
            'linear_inverse_a_coordinate_problem': self.linear_inverse_a_coordinate_problem,
            'linear_inverse_ab_length_problem': self.linear_inverse_ab_length_problem,
            'linear_inverse_area_problem': self.linear_inverse_area_problem,
            'unknown_parabola': self.unknown_parabola
        }

        handler = functions_handlers.get(current_sub_topic)
        if handler:
            self.problem, self.solution = handler()
        else:
            print(f"Warning: Unhandled state '{current_sub_topic}'")

    def get_problem_and_solution(self):
        return self.problem, self.solution

    @staticmethod
    def hyperbola_unknown_p_and_q_problem():
        p = _random_non_zero(-5, 5)
        q = _random_non_zero(-5, 5)
        question = f"\nHieronder is die grafiek van" \
                   f"\n$h(x) = \\frac{{1}}{{x+p}}+q$ geskets." \
                   f"\nDie asimptote van h sny by ({-p}; {q})." \
                   f"\n\nWat is die waardes van p en q?"

        solution = f"p = {p}, q = {q}\n\nAs jy dalk p as -{p} gekry het.\nOnthou as die vertikale asimptoot" \
                   f" positief is, \nis p negatief en 'vice versa'."
        _plot_hyperbola(p, q, question)

        return question, solution

    @staticmethod
    def hyperbola_x_intercept_problem():
        p = _random_non_zero(-5, 5)
        q = _random_non_zero(-5, 5)
        question = f"\nHieronder is die grafiek van" \
                   f"\n$h(x) = \\frac{{1}}{{x {_prettify_number(p, True)}}}+{q}$ geskets." \
                   f"\nBereken die x-afsnit van h."

        solution = f"\nOm die x-afsnit te kry, stel ons $y = 0$\n" \
                   f"$0 = \\frac{{{1}}}{{x {_prettify_number(p, True)}}}  {_prettify_number(q, True)}$\n" \
                   f"${-q} = \\frac{{{1}}}{{x {_prettify_number(p, True)}}}$\n" \
                   f"$\\frac{{{1}}}{{{-q}}} = x {_prettify_number(p, True)}$\n" \
                   f"$\\frac{{{1}}}{{{-q}}} {_prettify_number(-p, True)} = x$\n" \
                   f"$x = {((1 / (-q)) - p).__round__(4)}$\n" \
                   f"Die koördinate is dus $({((1 / (-q)) - p).__round__(4)}; 0)$"

        _plot_hyperbola(p, q, question)

        return question, solution

    @staticmethod
    def new_parabola_from_old_problem():
        p = _random_non_zero(-5, 5)
        q = _random_non_zero(-5, 5)
        added_number = _random_non_zero(-5, 5)
        question = f"\nHieronder is die grafiek van" \
                   f"\n$h(x) = \\frac{{1}}{{x {_prettify_number(p, True)}}} {_prettify_number(q, True)}$ geskets." \
                   f"\n\nBereken die x-afsnit van g as g = h(x {_prettify_number(added_number, True)})."

        _plot_hyperbola(p, q, question)

        # reassign p to new p value
        p2 = p + added_number
        solution = f"\n$g(x) = \\frac{{{1}}}{{x {_prettify_number(p, True)} {_prettify_number(added_number, True)}}} + {q}$" \
                   f"\nOm die x-afsnit te kry, stel ons $g(x) = 0$\n" \
                   f"$0 = \\frac{{{1}}}{{x {_prettify_number(p2, True)}}} + {q}$\n" \
                   f"${-q} = \\frac{{{1}}}{{x {_prettify_number(p2, True)}}}$\n" \
                   f"$\\frac{{{1}}}{{{-q}}} = x {_prettify_number(p2, True)}$\n" \
                   f"$\\frac{{{1}}}{{{-q}}} {_prettify_number(-p2, True)} = x$\n" \
                   f"$x = {((1 / (-q)) - p2).__round__(4)}$\n" \
                   f"Die koördinate is dus $({((1 / (-q)) - p2).__round__(4)}; 0)$"

        return question, solution

    @staticmethod
    def hyperbola_axis_of_symmetry_problem():
        p = _random_non_zero(-5, 5)
        q = _random_non_zero(-5, 5)
        question = f"\nHieronder is die grafiek van" \
                   f"\n$h(x) = \\frac{{1}}{{x {_prettify_number(p, True)}}} {_prettify_number(q)}$ geskets." \
                   f"\nDie vergelyking van 'n as van simmetrie vir h is:" \
                   f"\ny = x + t. Bepaal die waarde van t."

        solution = f"\nDie as van simmetrie moet deur $({-p}; {q})$\n gaan [Die snypunt van die asimptote]\n" \
                   f"Daarom vervang ons eenvoudig $({-p}; {q})$\n in $y = x + t$, dan los ons op vir $t$\n" \
                   f"${q} = {-p} + t$\n" \
                   f"${q} {_prettify_number(p, True)} = t$\n" \
                   f"$t = {q + p}$"

        _plot_hyperbola(p, q, question)
        return question, solution

    @staticmethod
    def hyperbola_inequality_question():
        p = _random_non_zero(-5, 5)
        q = _random_non_zero(-5, 5)
        sign = random.choice(["<", ">"])
        question = f"\nHieronder is die grafiek van" \
                   f"\n$h(x) = \\frac{{1}}{{x {_prettify_number(p, True)}}} {_prettify_number(q, True)}$ geskets." \
                   f"\nDie x-afsnit koördinate is: ({(1 / (-q) - p).__round__(4)}; 0)" \
                   f"\n\nBepaal die waarde van x waar:" \
                   f"\n${-q} {sign} \\frac{{1}}{{x {_prettify_number(p, True)}}}$"

        _plot_hyperbola(p, q, question)
        if sign == "<" and q > 0:
            solution = f"\nAs ons die ongelykheid her rangskik sien ons dat " \
                       f"\nhulle eintlik net vra waar die funksie groter is as 0." \
                       f"\n$0 < \\frac{{1}}{{x {_prettify_number(p, True)}}} {_prettify_number(q)}$" \
                       f"\n$0 < h(x)$\n" \
                       f"$x < {(1 / (-q) - p).__round__(4)}$ en $x > {-p}$; $x \\in \\mathbb{{R}}$"
        elif sign == ">" and q > 0:
            solution = f"\nAs ons die ongelykheid her rangskik sien ons dat " \
                       f"\nhulle eintlik net vra waar die funksie kleiner is as 0." \
                       f"\n$0 > \\frac{{1}}{{x {_prettify_number(p, True)}}} {_prettify_number(q)}$" \
                       f"$0 > h(x)$\n" \
                       f"${(1 / (-q) - p).__round__(4)} < x < {-p}$; $x \\in \\mathbb{{R}}$"
        elif sign == "<" and q < 0:
            solution = f"\nAs ons die ongelykheid her rangskik sien ons dat " \
                       f"\nhulle eintlik net vra waar die funksie groter is as 0." \
                       f"\n$0 < \\frac{{1}}{{x {_prettify_number(p, True)}}} {_prettify_number(q)}$" \
                       f"$0 < h(x)$\n" \
                       f"${-p} < x < {(1 / (-q) - p).__round__(4)}$; $x \\in \\mathbb{{R}}$"
        else:
            solution = f"\nAs ons die ongelykheid her rangskik sien ons dat " \
                       f"\nhulle eintlik net vra waar die funksie kleiner is as 0." \
                       f"\n$0 > \\frac{{1}}{{x {_prettify_number(p, True)}}} {_prettify_number(q)}$" \
                       f"$0 > h(x)$\n" \
                       f"$x < {p}$ en $x > {(1 / (-q) - p).__round__(4)}$; $x \\in \\mathbb{{R}}$"

        print(solution)
        return question, solution

    @staticmethod
    def para_expo_c_problem():
        a_par, b_par, c, a_exp, b_exp, q = _gen_connected_parabola_and_exponential_graph()
        question = f"Die grafieke van $f(x) = {a_par}x^2 {_prettify_number(b_par)}x {_prettify_number(c, True)}$" \
                   f" en $g(x) = {a_exp}.b^x + q$ is hieronder geskets." \
                   f"\n- C is die y-afsnit van f en lê op die asimptoot van g." \
                   f"\n\nGee die y-koördinaat van C."

        _plot_exponential_and_parabola(a_exp, b_exp, q, a_par, b_par, c, question, add_c=True)
        solution = f"\nDie Y-koördinaat vir C is {c}" \
                   f"\n(Die c waarde van die parabool is sy y-afsnit)"
        return question, solution

    @staticmethod
    def para_expo_d_problem():
        a_par, b_par, c, a_exp, b_exp, q = _gen_connected_parabola_and_exponential_graph()
        question = f"Die grafiek van $f(x) = {a_par}x^2 {_prettify_number(b_par)}x {_prettify_number(c, True)}$" \
                   f" en $g(x) = {a_exp}.b^x + q$ is hieronder geskets." \
                   f"\n- Die twee grafieke sny by D, wat die draaipunt van f is." \
                   f"\n\nBepaal die koördinate van D."

        _plot_exponential_and_parabola(a_exp, b_exp, q, a_par, b_par, c, question, add_d=True)
        tpx = -b_par / (2 * a_par)
        tpy = a_par * (tpx ** 2) + b_par * tpx + c
        solution = f"Om D se koördinate te kry moet ons die draaipunt van f vind." \
                   f"\nDie x-koördinaat van die draaipunt kan gevind word deur $dp_x = \\frac{{-b}}{{2a}}$\n" \
                   f"of deur die vierkant te voltooi vir die parabool\n" \
                   f"vervang $dp_x$ in $f(x)$ om die y-koördinaat te kry\n" \
                   f"Die koördinate van D is dus $({tpx}; {tpy})$"

        return question, solution

    @staticmethod
    def para_expo_b_and_q_problem():
        a_par, b_par, c, a_exp, b_exp, q = _gen_connected_parabola_and_exponential_graph()
        tpx = -b_par / (2 * a_par)
        tpy = a_par * (tpx ** 2) + b_par * tpx + c
        question = f"\nDie grafieke van $f(x) = {a_par}x^2 {_prettify_number(b_par)}x {_prettify_number(c, True)}$" \
                   f" en $g(x) = {a_exp}.b^x + q$ is hieronder geskets." \
                   f"\n- C is die y-afsnit van f en lê op die asimptoot van g." \
                   f"\n- Die twee grafieke sny by D, wat die draaipunt van f is." \
                   f"\n- Die koördinate van D is ({tpx}; {tpy})." \
                   f"\n\nBepaal die waardes van b en q."

        _plot_exponential_and_parabola(a_exp, b_exp, q, a_par, b_par, c, question, add_c=True, add_d=True)

        solution = f"\n$q = {c}$ (Die waarde van die konstante in $f(x)$)\n" \
                   f"Om $b$ te kry, sal ons punt D in $g(x)$ inlas\n" \
                   f"$g({tpx}) = {tpy} = {a_exp} \\cdot b^{{{tpx}}} {_prettify_number(c, True)}$\n" \
                   f"${tpy} {_prettify_number(-c, True)} = {a_exp} \\cdot b^{{{tpx}}}$\n" \
                   f"$\\frac{{ {tpy} {_prettify_number(-c, True)} }}{{ {a_exp} }} = b^{{{tpx}}}$\n" \
                   f"${(tpy - c) / a_exp}^{{1 / {tpx}}} = b$\n" \
                   f"$b = {b_exp.__round__(2)}$"

        return question, solution

    @staticmethod
    def para_expo_g_range_problem():
        a_par, b_par, c, a_exp, b_exp, q = _gen_connected_parabola_and_exponential_graph()
        tpx = -b_par / (2 * a_par)
        tpy = a_par * (tpx ** 2) + b_par * tpx + c
        question = f"\nDie grafieke van $f(x) = {a_par}x^2 {_prettify_number(b_par)}x {_prettify_number(c, True)}$" \
                   f" en $g(x) = {a_exp}.b^x + q$ is hieronder geskets." \
                   f"\n- C is die y-afsnit van f en lê op die asimptoot van g." \
                   f"\n- Die twee grafieke sny by D, wat die draaipunt van f is." \
                   f"\n- Die koördinate van D is ({tpx}; {tpy})." \
                   f"\n\nGee die waardeversameling van g."

        _plot_exponential_and_parabola(a_exp, b_exp, q, a_par, b_par, c, question, add_c=True, add_d=True)

        if a_exp > 0:
            solution = f"\nDie waardeversameling vir g is:\n" \
                       f"y ∈ ({q}, ∞)"
        else:
            solution = f"\nDie waardeversameling vir g is:\n" \
                       f"y ∈ (-∞, {q})"

        print(solution)
        return question, solution

    @staticmethod
    def adding_k_to_f_problem():
        a_par, b_par, c, a_exp, b_exp, q = _gen_connected_parabola_and_exponential_graph()
        tpx = -b_par / (2 * a_par)
        tpy = a_par * (tpx ** 2) + b_par * tpx + c
        if a_par > 0:
            question = f"\nDie grafieke van $f(x) = {a_par}x^2 {_prettify_number(b_par)}x {_prettify_number(c, True)}$" \
                       f" en $g(x) = {a_exp}.b^x + q$ is hieronder geskets." \
                       f"\n- C is die y-afsnit van f en lê op die asimptoot van g." \
                       f"\n- Die twee grafieke sny by D, wat die draaipunt van f is." \
                       f"\n- Die koördinate van D is ({tpx}; {tpy})." \
                       f"\nBepaal die waardes van K waarvoor die waarde van f(x) - K altyd positief sal wees."

            solution = f"\nDink aan $f(x) - k$ as 'n nuwe funksie $h(x)$\n" \
                       f"Sodat alle waardes van $h(x)$ positief is\n" \
                       f"moet ons verseker dat $k$ kleiner is as die keerpunt\n" \
                       f"se y-koördinaat. Daarom:\n" \
                       f"$k < {q}$; $k \\in \\mathbb{{R}}$"


        else:
            question = f"\nDie grafieke van $f(x) = {a_par}x^2 {_prettify_number(b_par)}x {_prettify_number(c, True)}$" \
                       f" en $g(x) = {a_exp}.b^x + q$ is hieronder geskets." \
                       f"\n- C is die y-afsnit van f en lê op die asimptoot van g." \
                       f"\n- Die twee grafieke sny by D, wat die draaipunt van f is." \
                       f"\n- Die koördinate van D is ({tpx}; {tpy})." \
                       f"\nBepaal die waardes van K waarvoor die waarde van f(x) - K altyd negatief sal wees."

            solution = f"\nDink aan $f(x) - k$ as 'n nuwe funksie $h(x)$\n" \
                       f"Sodat alle waardes van $h(x)$ negatief is\n" \
                       f"moet ons verseker dat $k$ groter is as die keerpunt\n" \
                       f"se y-koördinaat. Daarom:\n" \
                       f"$k > {q}$; $k \\in \\mathbb{{R}}$"

        _plot_exponential_and_parabola(a_exp, b_exp, q, a_par, b_par, c, question, add_c=True, add_d=True)

        print(solution)
        return question, solution

    @staticmethod
    def linear_inverse_c_problem():
        randomnumber = random.choice([1, 2])
        if randomnumber == 1:
            m = _random_non_zero(2, 5)
        else:
            m = _random_non_zero(-5, -2)
        c = _random_non_zero(-8, 8)

        question = f"\nDie grafiek van g(x) = {m}x {_prettify_number(c, True)} en \n$g^{{(-1)}}$, " \
                   f"die inverse van g, is hieronder geskets." \
                   f"\n- D en B is die x- en y-afsnitte van g." \
                   f"\n- C is die x-afsnit van $g^{{(-1)}}$." \
                   f"\n- Die grafiek van g en $g^{{(-1)}}$ sny by A." \
                   f"\n\nGee die koördinate van B."

        solution = f"\nDie koördinate vir B is (0, {c})"

        _plot_linear_and_inverse(m, c, question)
        return question, solution

    @staticmethod
    def linear_inverse_equation_problem():
        randomnumber = random.choice([1, 2])
        if randomnumber == 1:
            m = _random_non_zero(2, 5)
        else:
            m = _random_non_zero(-5, -2)
        c = _random_non_zero(-8, 8)

        question = f"\nDie grafiek van g(x) = {m}x {_prettify_number(c, True)} en \n$g^{{(-1)}}$, " \
                   f"die inverse van g, is hieronder geskets." \
                   f"\n- D en B is die x- en y-afsnitte van g." \
                   f"\n- C is die x-afsnit van $g^{{(-1)}}$." \
                   f"\n- Die grafiek van g en $g^{{(-1)}}$ sny by A." \
                   f"\n\nBepaal die vergelyking van $g^{{-1}}$ in die vorm $g^{{-1}}(x) = mx + n$."

        solution = f"Ruil die $x$ en $y$ om van $g(x)$. \n" \
                   f"$x = {m}y {_prettify_number(c, True)}$\n" \
                   f"$x {_prettify_number(-c, True)} = {m}y$\n" \
                   f"$\\frac{{x {_prettify_number(-c, True)}}}{{m}} = y$\n" \
                   f"$g^{{-1}}(x) = \\frac{{1}}{{m}}x - \\frac{{{c}}}{{m}}$"

        _plot_linear_and_inverse(m, c, question)
        return question, solution

    @staticmethod
    def linear_inverse_a_coordinate_problem():
        randomnumber = random.choice([1, 2])
        if randomnumber == 1:
            m = _random_non_zero(2, 5)
        else:
            m = _random_non_zero(-5, -2)
        c = _random_non_zero(-8, 8)

        x1 = (-(c / m) - c) / (m - (1 / m))
        question = f"\nDie grafiek van g(x) = {m}x {_prettify_number(c, True)} en \n$g^{{(-1)}}$, " \
                   f"die inverse van g, is hieronder geskets." \
                   f"\n- D en B is die x- en y-afsnitte van g." \
                   f"\n- C is die x-afsnit van $g^{{(-1)}}$." \
                   f"\n- Die grafiek van g en $g^{{(-1)}}$ sny by A." \
                   f"\n\nBepaal die koördinate van A."

        solution = f"Stel $g(x) = g^{{-1}}(x)$ gelyk\n" \
                   f"${m}x {_prettify_number(c, True)} = \\frac{{1}}{{{m}}}x - \\frac{{{c}}}{{{m}}}$\n" \
                   f"${m}x - \\frac{{1}}{{{m}}}x = - \\frac{{{c}}}{{{m}}} - {c}$\n" \
                   f"$x({m} - \\frac{{1}}{{{m}}}) = -\\frac{{{c}}}{{{m}}} - {c}$\n" \
                   f"$x = \\frac{{-\\frac{{{c}}}{{{m}}} - {c}}}{{{m} - \\frac{{1}}{{{m}}}}}$\n" \
                   f"\n$x = {x1}" \
                   f"Om die y-koördinaat te kry, plaas die x in $g(x)$\n" \
                   f"$g({x1.__round__(2)}) = {m.__round__(2)} \\times {x1.__round__(2)} + {c.__round__(2)}$\n" \
                   f"$g({x1.__round__(2)}) = {(m * x1 + c).__round__(2)}$\n" \
                   f"Die koördinate is dus: $({x1.__round__(2)}; {(m * x1 + c).__round__(2)})$"

        _plot_linear_and_inverse(m, c, question)
        return question, solution

    @staticmethod
    def linear_inverse_ab_length_problem():
        randomnumber = random.choice([1, 2])
        if randomnumber == 1:
            m = _random_non_zero(2, 5)
        else:
            m = _random_non_zero(-5, -2)
        c = _random_non_zero(-8, 8)

        x1 = (-(c / m) - c) / (m - (1 / m))
        y1 = m * x1 + c
        question = f"\nDie grafieke van g(x) = {m}x {_prettify_number(c, True)} en \n$g^{{(-1)}}(x)$ = ({(1 / m).__round__(2)})x - {(c / m).__round__(2)}," \
                   f" die inverse van g, is hieronder geskets." \
                   f"\n- D en B is die x- en y-afsnitte van g." \
                   f"\n- C is die x-afsnit van $g^{{(-1)}}$." \
                   f"\n- Die grafiek van g en $g^{{(-1)}}$ sny by A. ({x1.__round__(2)}; {y1.__round__(2)})" \
                   f"\n\nBereken die lengte van AB."

        solution = f"\nKoördinate van A is $({x1.__round__(2)}; {y1.__round__()})$\n" \
                   f"Koördinate van B is $(0; {c.__round__(2)})$\n" \
                   f"Gebruik die afstandformule:\n" \
                   f"$d = \\sqrt{{({x1.__round__(2)}- 0)^2 + ({y1.__round__(2)} - {c.__round__(2)})^2}}$\n" \
                   f"$d = \\sqrt{{ {(x1 ** 2).__round__(2)} + ({(y1 - c).__round__(2)})^2 }}$\n" \
                   f"$d = \\sqrt{{ {(x1 ** 2 + (y1 - c) ** 2).__round__(2)} }}$\n" \
                   f"$d = {((x1 ** 2 + (y1 - c) ** 2) ** 0.5).__round__(2)}$"

        _plot_linear_and_inverse(m, c, question)
        return question, solution

    @staticmethod
    def linear_inverse_area_problem():
        randomnumber = random.choice([1, 2])
        if randomnumber == 1:
            m = _random_non_zero(2, 5)
        else:
            m = _random_non_zero(-5, -2)
        c = _random_non_zero(-8, 8)

        x1 = (-(c / m) - c) / (m - (1 / m))
        y1 = m * x1 + c

        x_new = (c - ((1 / m) * c)) / ((1 / -m) - m)
        y_new = m * x_new + c

        d = (((x_new - c) ** 2) + ((y_new - 0) ** 2)) ** 0.5
        question = f"\nDie grafieke van g(x) = {m}x {_prettify_number(c, True)} en \n$g^{{(-1)}}(x)$ = ({(1 / m).__round__(2)})x - {(c / m).__round__(2)}" \
                   f" die inverse van g, is geskets hieronder.\n" \
                   f"- D en B is die x- en y-afsnitte van g.\n" \
                   f"- C is die x-afsnit van $g^{{(-1)}}$.\n" \
                   f"- Die lengte van AB = {((x1 ** 2 + (y1 - c) ** 2) ** 0.5).__round__(4)}\n\n" \
                   f"Bereken die area van driehoek ABC."

        solution = f"Eers, konstrueer 'n nuwe lyn wat loodreg op $g(x)$ is\n" \
                   f" en gaan deur punt C om die loodregte\n" \
                   f" hoogte van driehoek ABC te kry. Gebruik AB as die basis.\n" \
                   f"Die nuwe lyn sal 'n gradient van $\\frac{{1}}{{{-m}}}$ hê\n" \
                   f"Voer punt C $({c}, 0)$ in die nuwe lynvergelyking in\n" \
                   f"$0 = \\frac{{1}}{{{-m}}}({c}) + c$\n" \
                   f"$c = \\frac{{1}}{{{m}}} \\times c$\n" \
                   f"Kry nou die kruispunt van die nuwe lyn en lyn AB (of $g(x)$)\n" \
                   f" $\\frac{{1}}{{{-m}}}x + \\frac{{1}}{{{m}}} \\times c = {m}x + {c}$\n" \
                   f"los op om $x = \\frac{{{c} - (\\frac{{1}}{{{m}}} \\times {c})}}{{\\frac{{1}}{{{-m}}} {- m}}}$ te kry\n" \
                   f"Voer in $g(x)$ in om $y = {y_new.__round__(4)}$ te kry\n" \
                   f"Bereken afstand tussen kruispunt en punt C\n" \
                   f"$d = \\sqrt{{({x_new.__round__(4)} - {c})^2+({y_new.__round__(4)} - 0)^2}}$\n" \
                   f"$d = {d.__round__(4)}$\n" \
                   f"die oppervlakte is dus gelyk aan $0,5 \\times AB \\times$ loodregte hoogte\n" \
                   f"oppervlakte = $0,5 \\times \\sqrt{{ {(x1 ** 2 + (y1 - c) ** 2).__round__(4)} }} \\times {d}$\n" \
                   f"oppervlakte = ${(0.5 * ((x1 ** 2 + (y1 - c) ** 2) ** 0.5) * d).__round__(4)}$"

        _plot_linear_and_inverse(m, c, question)
        return question, solution

    @staticmethod
    def unknown_parabola():
        a, b, c, r1, r2 = _gen_factored_quadratic()
        while b == 0:
            a, b, c, r1, r2 = _gen_factored_quadratic()

        question = f"\nDie grafiek van $f'(x) = mx^2 + nx + k$ is hieronder geskets.\n" \
                   f"Die grafiek gaan deur die punte:\n" \
                   f"P({r1}; 0), Q({r2}, 0) en R(0; {c}).\n\n" \
                   f"Bepaal die waardes van m, n and k."

        solution = f"\nk = {c} (die y-snit van die parabool)" \
                   f"\nAangesien ons die wortels weet (gegee deur punt P en Q)\n" \
                   f"kan ons die gefaktoriseerde hakies so opstel:\n" \
                   f"m(x {_prettify_number(-r1, True)})(x {_prettify_number(-r2, True)}) = mx^2 + nx + ({c})\n" \
                   f"As ons dit uitbrei, sal ons 2 vergelykings kry wat ons kan gebruik om n en m op te los\n" \
                   f"mx^2 + {r1 + r2}mx + {r1 * r2}m = mx^2 + nx + ({c})\n" \
                   f"Ons kan nou sien dat {r1 + r2}m = n en {r1 * r2}m = k = {c}\n" \
                   f"Daarom is m = {c / (r1 * r2)} en daarom is n = {(r1 + r2) * (c / (r1 * r2))}"

        _plot_single_parabola(a, b, c, r1, r2, question)
        print(solution)
        return question, solution


############################################################
# Probability


def _generate_venn_diagram(a, b, c, ab, ac, bc, abc, total, outside_probability, question):
    # Pack sizes into a tuple
    set_sizes = (a / 100, b / 100, ab / 100, c / 100, ac / 100, bc / 100, abc / 100)

    venn = venn3(subsets=set_sizes)

    # Label the sets
    venn.get_label_by_id('100').set_text(f'{(a - ab - ac - abc) / 100}')
    venn.get_label_by_id('010').set_text(f'{((b - ab - bc - abc) / 100).__round__(4)}')
    venn.get_label_by_id('001').set_text(f'{(c - ac - bc - abc) / 100}')
    venn.get_label_by_id('111').set_text('x')
    # Optional: Customize the plot
    plt.title(f"A, B, en C is drie gebeurtenisse."
              f"\nDie waarskynlikhede dat die gebeurtenisse (of enige kombinasie van hulle)"
              f"\nsal plaasvind, is gegee in die Venn-diagram hieronder."
              f"\n\n {question}", y=1.05)
    # Add 'y' outside the circles to represent the probability of none of the events occurring
    plt.text(0.8, 0, 'y', ha='left', va='center', fontsize=12, color='red')

    plt.tight_layout()
    plt.savefig("/tmp/output.png", bbox_inches='tight')

    # Optionally, close the plot to free up memory
    plt.close()


def _generate_3_set_venn_variebles():
    ab_independent = random.choice([True, False])

    abc = random.randint(1, 5)
    ac = abc + random.randint(1, 10)
    bc = abc + random.randint(1, 10)
    ab = abc + random.randint(1, 10)

    # Generate sizes for individual sets
    a = ab + ac + abc + random.randint(10, 20)
    if ab_independent:
        b = (ab / 100) * (100 / a) * 100
    else:
        b = ab + bc + abc + random.randint(10, 20)
    c = ac + bc + abc + random.randint(10, 20)

    total = ab + bc + ac + abc + (a - ab - ac - abc) + (b - ab - bc - abc) + (c - ac - bc - abc)
    outside_probability = 100 - total

    return a, b, c, ab, ac, bc, abc, total, outside_probability


class Probability:
    def __init__(self, current_sub_topic):

        probability_handlers = {
            'event_not_occurring_problem': self.event_not_occurring_problem,
            'abc_intersection_problem': self.abc_intersection_problem,
            'determine_at_least_two_events_problem': self.determine_at_least_two_events_problem,
            'are_events_independent': self.are_events_independent,
            'combination_problem': self.combination_problem,
            'another_combination_problem': self.another_combination_problem
        }

        handler = probability_handlers.get(current_sub_topic)
        if handler:
            self.problem, self.solution = handler()
        else:
            print(f"Warning: Unhandled state '{current_sub_topic}'")

    def get_problem_and_solution(self):
        return self.problem, self.solution

    @staticmethod
    def event_not_occurring_problem():
        a, b, c, ab, ac, bc, abc, total, outside_probability = _generate_3_set_venn_variebles()
        problem = f"\nAs dit gegee word dat die waarskynlikheid dat ten minste \neen van die gebeurtenisse sal plaasvind {total / 100} is," \
                  f" bereken y, \ndie waarskynlikheid dat geen van die gebeurtenisse sal plaasvind nie."

        solution = f"\n1 - (waarskynlikheid van minstens een gebeurtenis)\n" \
                   f"=1 - {total / 100}\n" \
                   f"= {1 - (total / 100)}"
        _generate_venn_diagram(a, b, c, ab, ac, bc, abc, total, outside_probability, problem)

        return problem, solution

    @staticmethod
    def abc_intersection_problem():
        a, b, c, ab, ac, bc, abc, total, outside_probability = _generate_3_set_venn_variebles()
        problem = f"\nAs dit gegee word dat die waarskynlikheid dat ten minste een van die gebeurtenisse sal plaasvind {total / 100} is,\n" \
                  f" bereken x, die waarskynlikheid dat al drie die gebeurtenisse sal plaasvind."
        solution = f"\nVoeg die waarskynlikheid van elke afdeling van die Venn-diagram by, behalwe die " \
                   f"waarskynlikheid dat geen gebeurtenisse sal plaasvind nie. Dit moet gelykstaande wees aan " \
                   f"die totale waarskynlikheid dat enige gebeurtenis sal plaasvind." \
                   f"\n{ab} + {ac} + {bc} + {a - ac - ab - abc} + {b - bc - ab - abc} " \
                   f"+ {c - ac - bc - abc} + x = {total / 100}\n" \
                   f"x = {total / 100} - ({ab} + {ac} + {bc} + {a - ac - ab - abc} + {b - bc - ab - abc}+ {c - ac - bc - abc})" \
                   f"\n x = {abc}"
        _generate_venn_diagram(a, b, c, ab, ac, bc, abc, total, outside_probability, problem)
        return problem, solution

    @staticmethod
    def determine_at_least_two_events_problem():
        a, b, c, ab, ac, bc, abc, total, outside_probability = _generate_3_set_venn_variebles()
        problem = f"\nAs dit gegee word dat die waarskynlikheid dat ten minste een van die gebeurtenisse sal plaasvind {total / 100} is,\n" \
                  f" bereken die waarskynlikheid dat ten minste twee van die gebeurtenisse sal plaasvind."
        solution = f"\nVoeg die waarskynlikheid van elke afdeling van die Venn-diagram by, behalwe die " \
                   f"waarskynlikheid dat geen gebeure sal plaasvind nie. Dit moet gelykstaan aan " \
                   f"die totale waarskynlikheid van enige gebeurtenis wat plaasvind. " \
                   f"\n{ab} + {ac} + {bc} + {a - ac - ab - abc} + {b - bc - ab - abc} " \
                   f"+ {c - ac - bc - abc} + x = {total / 100}\n" \
                   f"x = {total / 100} - ({ab} + {ac} + {bc} + {a - ac - ab - abc} + {b - bc - ab - abc}+ {c - ac - bc - abc})" \
                   f"\n x = {abc}" \
                   f"\n p(ten minste twee) = p(ab) + p(ac) + p(bc) + p(abc)" \
                   f"\n p(ten minste twee) = {ab / 100} + {ac / 100} + {bc / 100} + {abc / 100}" \
                   f"\n p(ten minste twee) = {(ab / 100) + (ac / 100) + (bc / 100) + (abc / 100)}"

        _generate_venn_diagram(a, b, c, ab, ac, bc, abc, total, outside_probability, problem)
        return problem, solution

    @staticmethod
    def are_events_independent():
        a, b, c, ab, ac, bc, abc, total, outside_probability = _generate_3_set_venn_variebles()
        problem = f"As dit gegee word dat die waarskynlikheid dat ten minste een van die gebeurtenisse sal plaasvind {total / 100} is.\n" \
                  f"\nBepaal of gebeurtenisse A en B onafhanklik is, staaf jou antwoord."
        if (ab / 100) == ((a / 100) * (b / 100)).__round__(4):
            solution = f"\nVir gebeurtenisse A en B om onafhanklik te wees moet, P(A∩B)=P(A)⋅P(B)" \
                       f"\nP(A∩B)= {ab / 100}" \
                       f"\nP(A)⋅P(B) = {a / 100}*{b / 100} = {(a / 100) * (b / 100)}" \
                       f"\ndus P(A∩B)=P(A)⋅P(B) en gebeurtenisse A en B is onafhanklik"
        else:
            solution = f"\nVir gebeurtenisse A en B om onafhanklik te wees moet, P(A∩B)=P(A)⋅P(B)" \
                       f"\nP(A∩B)= {ab / 100}" \
                       f"\nP(A)⋅P(B) = {a / 100}*{b / 100} = {(a / 100) * (b / 100)}" \
                       f"\ndus is P(A∩B) nie gelyk aan P(A)⋅P(B) nie en gebeurtenisse A en B is nie onafhanklik nie."
        _generate_venn_diagram(a, b, c, ab, ac, bc, abc, total, outside_probability, problem)
        return problem, solution

    @staticmethod
    def combination_problem():
        n_digits = random.randint(4, 5)
        even_or_odd = random.choice(['ewe', 'onewe'])
        exclusion1 = random.randint(0, 9)
        exclusion2 = random.randint(0, 9)
        while exclusion1 == exclusion2:
            exclusion2 = random.randint(0, 9)
        may_be_repeated = random.choice([True, False])

        possible_set = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
        possible_set.discard(exclusion1)
        possible_set.discard(exclusion2)

        if even_or_odd == 'onewe':
            possible_d1_set = {1, 3, 5, 7, 9}
            possible_d1_set.discard(exclusion1)
            possible_d1_set.discard(exclusion2)
            position1_possibilities = len(possible_d1_set)
        else:
            possible_d1_set = {0, 2, 4, 6, 8}
            possible_d1_set.discard(exclusion1)
            possible_d1_set.discard(exclusion2)
            position1_possibilities = len(possible_d1_set)

        total_comb = position1_possibilities
        possible_comb = []
        for i in range(n_digits - 1):
            possible_comb.append(len(possible_set) - 1 - i)
            total_comb = total_comb * possible_comb[i]

        if n_digits == 5:
            maybe_then_4 = ", then 4"
            maybe_4 = "⋅4"
        else:
            maybe_then_4 = ""
            maybe_4 = ""

        problem = f"\n'n {n_digits}-Syfer kode word benodig om 'n kombinasie-slot oop te maak.\n" \
                  f"Die kode moet 'n {even_or_odd} nommer wees en mag nie die syfers\n" \
                  f"{exclusion1} en {exclusion2} bevat nie. Syfers mag nie herhaal word nie.\n" \
                  f"Hoeveel moontlike {n_digits}-syfer kombinasies is daar om die slot oop te maak?"
        solution = f"\nEerstens moet ons begin deur die moontlike syfers vir die laaste plek " \
                   f"of eenhede in die getal te bepaal.\n" \
                   f"Aangesien dit 'n '{even_or_odd}' getal is, weet ons dat daar {len(possible_d1_set)} " \
                   f"moontlike syfers is, naamlik {str(possible_d1_set).strip('{}')}.\n" \
                   f"Nou vir die ander syfers sal ons begin met 7 moontlike syfers oor, dan 6, dan 5" \
                   f"{maybe_then_4}.\n" \
                   f"Dus sal die totale aantal kombinasies wees: 7⋅6⋅5{maybe_4}⋅{len(possible_d1_set)}\n" \
                   f"Dit gee vir ons 'n totaal van {total_comb} kombinasies."

        generate_picture("", problem)
        return problem, solution

    @staticmethod
    def another_combination_problem():
        n_digits = random.randint(4, 5)
        even_or_odd = random.choice(['ewe', 'onewe'])
        exclusion1 = random.randint(0, 9)
        exclusion2 = random.randint(0, 9)
        while exclusion1 == exclusion2:
            exclusion2 = random.randint(0, 9)
        may_be_repeated = random.choice([True, False])
        greater_or_smaller = random.choice(["groter", "kleiner"])
        number = random.randint(1, 9) * (10 ** (n_digits - 1))
        second_or_third = random.choice(['twede', 'derde'])

        possible_set = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
        possible_set.discard(exclusion1)
        possible_set.discard(exclusion2)

        if even_or_odd == 'onewe':
            possible_d1_set = {1, 3, 5, 7, 9}
            possible_d1_set.discard(exclusion1)
            possible_d1_set.discard(exclusion2)
            position1_possibilities = len(possible_d1_set)
        else:
            possible_d1_set = {0, 2, 4, 6, 8}
            possible_d1_set.discard(exclusion1)
            possible_d1_set.discard(exclusion2)
            position1_possibilities = len(possible_d1_set)

        second_or_third_number = random.choice(list(possible_set))
        possible_set.discard(second_or_third_number)

        problem = f"\n'n {n_digits}-Syfer kode word benodig om 'n kombinasie-slot oop te maak.\n" \
                  f"Die kode moet 'n {even_or_odd} nommer wees en mag nie die syfers\n" \
                  f"{exclusion1} en {exclusion2} bevat nie. Syfers mag nie herhaal word nie.\n" \
                  f"\nBereken die waarskynlikheid dat jy die slot sal oopmaak op jou \n" \
                  f"eerste poging as dit verder gegee word dat die kode {greater_or_smaller} as " \
                  f"\n{number} is en die {second_or_third} syfer is {second_or_third_number}."
        generate_picture("", problem)

        possible_set_first_digit = set()
        if greater_or_smaller == "groter":
            for i in range(int(number / (10 ** (n_digits - 1))), 10):
                possible_set_first_digit.add(i)
        else:
            for i in range(1, int(number / (10 ** (n_digits - 1)))):
                possible_set_first_digit.add(i)

        common_between_first_and_last = possible_set_first_digit.intersection(possible_d1_set)
        additional_combinations = 0
        if n_digits == 4:
            combinations1 = len(possible_d1_set) * (
                    len(possible_set_first_digit) - len(common_between_first_and_last)) * 5
            for i in range(len(common_between_first_and_last)):
                additional_combinations = additional_combinations + ((len(possible_d1_set) - 1) * 5)
        else:
            combinations1 = len(possible_d1_set) * (
                    len(possible_set_first_digit) - len(common_between_first_and_last)) * 5 * 4
            for i in range(len(common_between_first_and_last)):
                additional_combinations = additional_combinations + ((len(possible_d1_set) - 1) * 5 * 4)

        total_combination = combinations1 + additional_combinations
        overall_prob = 1 / total_combination

        if n_digits == 5:
            maybe_then_4 = ", then 4"
            maybe_4 = "⋅4"
        else:
            maybe_then_4 = ""
            maybe_4 = ""

        solution = f"\nVir hierdie probleem sal ons die moontlike kombinasies in twee dele moet opdeel\n" \
                   f"Eerstens sal ons die aantal kombinasies moet bereken waar ons seker is dat die \n" \
                   f"eerste syfer nie 'n moontlikheid vir die laaste syfer is nie. Byvoorbeeld as die moontlike\n" \
                   f"syfers vir die eerste plek 1, 2, 3 en 4 is en die moontlike syfers vir die laaste\n" \
                   f"plek is 2, 6 en 8. Dan sal ons 2 as 'n moontlikheid vir die eerste plek moet uitsluit.\n" \
                   f"2 as 'n moontlikheid vir die eerste plek sal dan heeltemal apart bereken word.\n" \
                   f"\n\nSo in hierdie spesifieke probleem sal ons begin met die moontlikhede vir die laaste plek\n" \
                   f"In hierdie geval is ons moontlikhede: {str(possible_d1_set).strip('{}')}\n" \
                   f"vir die eerste plekke het ons moontlikhede: {str(possible_set_first_digit).strip('{}')}\n" \
                   f"maar ons sal eerste enige ooreenkoms tussen die eerste en laaste syfer moontlikhede uitsluit:\n" \
                   f"{str(common_between_first_and_last).strip('{}')}\n" \
                   f"Ons weet dat die '{second_or_third}' syfer {second_or_third_number} is en daarom het dit net \n" \
                   f"een moontlikheid. Die ander syfers het dus 5{maybe_then_4} kombinasies.\n" \
                   f"Dus kan die eerste deel bereken word as " \
                   f"{len(possible_set_first_digit) - len(common_between_first_and_last)}⋅5{maybe_4}⋅{len(possible_d1_set)}" \
                   f" = {combinations1} \n(Hier sluit ek syfers met net 1 moontlikheid uit vir voor die hand liggende redes)\n\n" \
                   f"Nou vir die tweede deel sal ons enige syfers vir die eerste syfer wat ons uitgesluit het, bereken as:\n" \
                   f"(5{maybe_4}⋅{len(possible_d1_set) - 1})⋅{len(common_between_first_and_last)} = {additional_combinations}" \
                   f" (weer eens, die syfers met net 1 moontlikheid is uitgesluit) \n" \
                   f"(maal die aantal syfers wat gemeenskaplik was tussen die eerste en laaste syfer moontlikhede)\n" \
                   f"laastens kry ons die totale moontlikhede om {total_combination} te wees en daarom is die waarskynlikheid\n" \
                   f"op 'n eerste poging: {overall_prob}"

        return problem, solution


############################################################
# Sequences and series


def _gen_arithmetic_sequence(progression_range=10, starting_range=10):
    progression_num = random.randint(-progression_range, progression_range)
    while progression_num == 0:
        progression_num = random.randint(-progression_range, progression_range)
    start_num = random.randint(-starting_range, starting_range)
    n = random.randint(5, 30)

    a = progression_num
    b = start_num - a

    t1 = start_num
    t2 = a * 2 + b
    t3 = a * 3 + b
    t4 = a * 4 + b
    t5 = a * 5 + b
    tn = a * n + b

    if a == 1:
        a = ''
    elif a == -1:
        a = '-'
    if b > 0:
        b = f"+ {b}"
    elif b < 0:
        b = abs(b)
        b = f"- {b}"

    rule = f"T_n = {a}n {b}"
    first_terms = f"{t1}, {t2}, {t3}, {t4}, {t5}"

    return {
        "n": n,
        "Tn": tn,
        "First_terms": first_terms,
        "rule": rule,
        "a": a,
        "b": b
    }


def _gen_geometric_sequence():
    r = random.randint(-2, 12)
    while r == 0:
        r = random.randint(-2, 11)
    start_num = random.randint(1, 6)
    n = random.randint(6, 14)

    tn = start_num * (r ** (n - 1))
    rule = f"{start_num} \cdot {r}^{{n-1}}"

    # f"{start_num} x {r}^(n-1)"
    first_terms = f"{start_num}, {start_num * (r)}, {start_num * (r ** 2)}, {start_num * (r ** 3)}, {start_num * (r ** 4)}"
    return {
        "n": n,
        "Tn": tn,
        "first_terms": first_terms,
        "rule": f"T_n = {rule}",
        "r": r,
        "a": start_num
    }


def _gen_geometric_small_r():
    r = random.randint(-6, 6)
    while r == 0 or r == 1 or r == -1:
        r = random.randint(-2, 11)
    start_num = random.randint(1, 6)
    n = random.randint(6, 12)

    tn = start_num * (r ** n)
    rule = f"\\frac{{1}}{{{start_num}}} \cdot \\left(\\frac{{1}}{{{r}}}\\right)^{{n}}"

    term_list = [0] * n
    for i in range(n):
        term_list[i] = f"\\frac{{1}}{{{start_num * (r ** (i + 1))}}}"

    return {
        "n": n,
        "Tn": f"\\frac{{1}}{{{tn}}}",
        "first_terms": ", ".join(term_list[0:5]),
        "rule": f"Tn = {rule}",
        "r": f"1/{r}",
        "a": f"1/{start_num}"
    }


def _gen_quadratic_sequence():
    a1 = random.randint(-5, 5)
    a2 = random.randint(-5, 5)
    x1 = random.randint(-5, 5)
    x2 = random.randint(-5, 5)
    while a1 == 0:
        a1 = random.randint(-5, 5)
    while a2 == 0:
        a2 = random.randint(-5, 5)
    while x1 == 0:
        x1 = random.randint(-5, 5)
    while x2 == 0:
        x2 = random.randint(-5, 5)

    a = a1 * a2
    b = a1 * x2 + a2 * x1
    c = x1 * x2

    a_string = f"{a}"
    if a == 1:
        a_string = ""

    b_string = f"+ {b}"
    if b == 1:
        b_string = "+ "
    elif b < 0:
        b_string = f"- {abs(b)}"

    c_string = f"+ {c}"
    if c < 0:
        c_string = f"- {abs(c)}"

    rule = f"T_n = {a_string}n^2 {b_string}n {c_string}"

    n = random.randint(6, 15)
    tn = a * (n ** 2) + b * n + c

    first_terms = []
    for i in range(5):
        first_terms.append((a * ((i + 1) ** 2) + b * (i + 1) + c))

    return {
        "n": n,
        "Tn": tn,
        "first_terms": (first_terms[0:5]),
        "rule": rule,
        "a": a,
        "b": b,
        "c": c
    }


def _gen_arithmetic_series(progression_range=10, starting_range=10):
    progression_num = random.randint(-progression_range, progression_range)
    start_num = random.randint(-starting_range, starting_range)
    n = random.randint(6, 40)

    a = progression_num
    b = start_num - a

    term_list = [0] * n
    sn = 0
    for i in range(n):
        term_list[i] = a * (i + 1) + b
        sn += term_list[i]

    if a == 1:
        a1 = ''
    elif a == -1:
        a1 = ''
    else:
        a1 = a
    if b > 0:
        b1 = f"+ {b}"
    elif b < 0:
        b1 = abs(b)
        b1 = f"- {b1}"
    else:
        b1 = b

    rule = f"\\sum_{{n=1}}^{n} {a1}n {b1}"

    return {
        "n": n,
        "Sn": sn,
        "First_terms": term_list,
        "rule": f"{rule}",
        "a": a,
        "b": b
    }


def _gen_geometric_series():
    r = random.randint(-2, 12)
    while r == 0:
        r = random.randint(-2, 12)
    start_num = random.randint(1, 12)
    n = random.randint(6, 20)

    term_list = [0] * n
    sn = 0
    for i in range(n):
        term_list[i] = start_num * (r ** (i))
        sn += term_list[i]

    rule = f"\\sum_{{i=1}}^{{{n}}} {start_num} \cdot {r}^{{i-1}}"
    return {
        "n": n,
        "Sn": sn,
        "First_terms": term_list,
        "rule": f"Sn = {rule}",
        "a": start_num,
        "r": r
    }


def _gen_geometric_series_small_r():
    r = random.randint(-6, 6)
    while r == 0 or r == 1 or r == -1:
        r = random.randint(-6, 6)
    start_num = random.randint(1, 12)
    n = random.randint(6, 20)

    term_list = [0] * n
    sn = 0
    for i in range(n):
        term_list[i] = f"\\frac{{1}}{{{start_num * (r ** i)}}}"
        sn += Fraction(1, start_num * (r ** i))

    rule = f"\\frac{{1}}{{{start_num}}} \cdot \\left(\\frac{{1}}{{{r}}}\\right)^{{n-1}}"
    sn = f"{sn.numerator}/{sn.denominator}"
    return {
        "n": n,
        "Sn": sn,
        "First_terms": term_list,
        "rule": f"Tn = {rule}",
        "r": Fraction(1, r),
        "a": Fraction(1, start_num)

    }


class SequencesAndSeries:
    def __init__(self, current_sub_topic):

        function_handlers = {
            'quadratic_unknown_rule_problem': self.quadratic_unknown_rule_problem,
            'quadratic_unknown_tn_problem': self.quadratic_unknown_tn_problem,
            'quadratic_unknown_n_problem': self.quadratic_unknown_n_problem,
            'quadratic_first_difference_sum_proof_problem': self.quadratic_first_difference_sum_proof_problem,
            'geometric_unknown_rule_problem': self.geometric_unknown_rule_problem,
            'geometric_unknown_tn_problem': self.geometric_unknown_tn_problem,
            'geometric_unknown_n_problem': self.geometric_unknown_n_problem,
            'geometric_list_first_terms_problem': self.geometric_list_first_terms_problem,
            'geometric_infinity_problem': self.geometric_infinity_problem,
            'sigma_expansion_problem': self.sigma_expansion_problem,
            'rewrite_to_sigma_problem': self.rewrite_to_sigma_problem,
            'arithmetic_series_to_n_problem': self.arithmetic_series_to_n_problem,
            'arithmetic_find_term_problem': self.arithmetic_find_term_problem,
            'arithmetic_first_five_terms_problem': self.arithmetic_first_five_terms_problem,
            'arithmetic_sequence_rule_problem': self.arithmetic_sequence_rule_problem,
            'values_for_convergence_problem': self.values_for_convergence_problem,
            'geometric_ratio_problem': self.geometric_ratio_problem,
            # 'geometric_series_ratio_problem': self.geometric_series_ratio_problem
        }

        handler = function_handlers.get(current_sub_topic)
        if handler:
            self.problem, self.solution = handler()
        else:
            print(f"Warning: Unhandled state '{current_sub_topic}'")

    def get_problem_and_solution(self):
        return self.problem, self.solution

    @staticmethod
    def quadratic_unknown_rule_problem():
        sequence = _gen_quadratic_sequence()
        generate_picture(str(sequence["first_terms"]).strip('[]').replace(",", "; "),
                         "\nBepaal die algemene term vir die volgende ry:")
        problem = f"Bepaal die algemene term vir die volgende ry: \n{str(sequence['first_terms']).strip('[]')}"
        solution = f"\n${sequence['rule']}$"

        return problem, solution

    @staticmethod
    def quadratic_unknown_tn_problem():
        sequence = _gen_quadratic_sequence()

        problem = f"\nWat is die waarde van die {sequence['n']}'de term in die volgende ry:\n\n{str(sequence['first_terms']).strip('[]').replace(',', '; ')}"
        solution = f"\nDie {sequence['n']}'de term = {sequence['Tn']}"

        generate_picture(str(sequence['first_terms']).strip('[]').replace(',', '; '),
                         f"\nWat is die waarde van die {sequence['n']}'de term in die volgende ry:")

        return problem, solution

    @staticmethod
    def quadratic_unknown_n_problem():
        sequence = _gen_quadratic_sequence()

        problem = f"\nWatter term in die volgende ry is gelyk aan {sequence['Tn']}:\n\n{sequence['first_terms']}"
        solution = f"\nDie {sequence['n']}'de term"

        generate_picture(str(sequence['first_terms']).strip('[]').replace(',', '; '),
                         f"\nWatter term in die volgende ry is gelyk aan {sequence['Tn']}?")

        return problem, solution

    @staticmethod
    def quadratic_first_difference_sum_proof_problem():
        sequence = _gen_quadratic_sequence()

        first_difference_pattern = []
        for i in range(4):
            first_difference_pattern.append(sequence["first_terms"][i + 1] - sequence["first_terms"][i])
        print(first_difference_pattern)

        a = first_difference_pattern[0]
        d = first_difference_pattern[1] - first_difference_pattern[0]
        q1 = d / 2
        q2 = a - q1

        if q1.is_integer():
            q1 = int(q1)
        if q2.is_integer():
            q2 = int(q2)
        if q2 > 0:
            q2 = f"+ {q2}"
        elif q2 < 0:
            q2 = f"- {abs(q2)}"
        elif q2 == 1:
            q2 = "+ "
        elif q2 == -1:
            q2 = "- "

        sum_formula = f"S_n = {(q1)}n^2 {q2}n"
        annotation = f"\nWys dat die som van die eerste n-hoeveelheid eerste-verskille van \ndie gegewe kwadratiese ry gegee kan word deur: " \
                     f" ${sum_formula}$ "
        quadratic_formula = sequence['rule']

        generate_picture(quadratic_formula, annotation)
        problem = f"\n{annotation}\n\n{quadratic_formula}"
        solution = f"\nDie student moet die volgende eerste n, eerste-verskilpatroon toon: {str(first_difference_pattern)}\n\n " \
                   f"Die student moet $a = {a}$ en $d = {d}$ toon\n\n Dan moet alle relevante waardes " \
                   f"ingeskakel word in die formule: $S_n = \\frac{{n}}{{2}}(2a + (n-1)d)$ om $S_n = \\frac{{n}}{{2}}({2 * a}+(n-1){d})$ te kry\n\n die formule moet dan uitgebrei en " \
                   f"vereenvoudig word om ${sum_formula}$ te kry "

        return problem, solution

    @staticmethod
    def geometric_unknown_rule_problem():
        r_determinant = random.randint(0, 2)
        if r_determinant == 0:
            geo_list = _gen_geometric_small_r()
        else:
            geo_list = _gen_geometric_sequence()

        generate_picture(geo_list['first_terms'], "Gee die reel vir 'n meetkundige ry met die volgende terme:")
        problem = f"\nGive the rule for a geometric sequence with the following terms: {geo_list['first_terms']}"
        solution = f"\n${geo_list['rule']}$"

        return problem, solution

    @staticmethod
    def geometric_unknown_tn_problem():
        r_determinant = random.randint(0, 2)
        if r_determinant == 0:
            geo_list = _gen_geometric_small_r()
        else:
            geo_list = _gen_geometric_sequence()
        generate_picture(geo_list['first_terms'], f"\nWat is die {geo_list['n']}'de term van die volgende ry:")
        problem = f"\nWat is die {geo_list['n']}'de term van die volgende ry:\n{geo_list['first_terms']}"
        solution = f"\nDie reël van die ry is ${geo_list['rule']}$ en die {geo_list['n']}'de term is gelyk aan {geo_list['Tn']}"
        return problem, solution

    @staticmethod
    def geometric_unknown_n_problem():
        r_determinant = random.randint(0, 2)
        if r_determinant == 0:
            geo_list = _gen_geometric_small_r()
        else:
            geo_list = _gen_geometric_sequence()
        generate_picture(geo_list['first_terms'],
                         f"\nWatter term is gelyk aan ${geo_list['Tn']}$ in die volgende ry:")
        problem = f"\nWatter term is gelyk aan {geo_list['Tn']} in die volgende ry:\n{geo_list['first_terms']}"
        solution = f"\nDie reël van die volgorde is ${geo_list['rule']}$ en die {geo_list['n']}'de term is gelyk aan {geo_list['Tn']}"
        return problem, solution

    @staticmethod
    def geometric_list_first_terms_problem():
        r_determinant = random.randint(0, 2)
        if r_determinant == 0:
            geo_list = _gen_geometric_small_r()
        else:
            geo_list = _gen_geometric_sequence()
        problem = f"\nLys die eerste 5 terme van 'n meetkundige ry met die volgende reel: {geo_list['rule']}"
        solution = f"\n{geo_list['first_terms']}"
        generate_picture(geo_list['rule'], f"\nLys die eerste 5 terme van 'n meetkundige ry met die volgende reel:")
        return problem, solution

    @staticmethod
    def geometric_infinity_problem():
        r_determanant = random.randint(-1, 10)
        if r_determanant < 0:
            g_series = _gen_geometric_series()
            solution = "\nDaar is geen oplossing nie, die reeks is nie-konvergerend"
        else:
            g_series = _gen_geometric_series_small_r()
            answer = Fraction(g_series['a'], 1 - g_series['r'])
            solution = f"\n${answer.numerator}/{answer.denominator}$"

        series_terms = ''
        for i in range(len(g_series["First_terms"])):
            series_terms += f"${g_series['First_terms'][i]}$ + "
        series_terms = series_terms.rstrip(" + ").strip("$")
        problem = f"\nBereken, waar van toepassing, die som van die volgende reeks tot oneindigheid:\n{series_terms}"
        generate_picture(series_terms,
                         f"\nBereken, waar van toepassing, die som van die volgende reeks tot oneindigheid:")
        return problem, solution

    @staticmethod
    def sigma_expansion_problem():
        type_of_series = random.randint(1, 2)
        if type_of_series == 1:
            series = _gen_geometric_series()
        else:
            series = _gen_arithmetic_series()
        problem = f"\nBereken die volgende: \n{series['rule']}\nWith n starting at 1 and ending at {series['n']}"
        answer = ''
        for i in range(series['n']):
            answer += f"{series['First_terms'][i]}+"
        answer = answer.strip().strip("+")
        solution = series['Sn']
        generate_picture(series['rule'], f"Bereken die volgende:")
        return problem, solution

    @staticmethod
    def rewrite_to_sigma_problem():
        # Choose arithmetic or geometric randomly
        if random.choice([True, False]):
            series = _gen_arithmetic_series()
            series_type = 'rekenkundige'
        else:
            series = _gen_geometric_series()
            series_type = 'meetkundige'

        # Format the series for the problem
        formatted_series = ' + '.join(str(term) for term in series['First_terms'])

        problem = f"\nHerskryf die volgende {series_type} reeks in sigma notasie: {formatted_series}"
        solution = f"\n${series['rule']}$"
        generate_picture(formatted_series, f"\nHerskryf die volgende {series_type} reeks in sigma notasie:")

        return problem, solution

    @staticmethod
    def arithmetic_series_to_n_problem():
        series = _gen_arithmetic_series()
        problem = f"\nBereken die som van die volgende reeks tot en met die {series['n']}'de term:\n{series['rule']}"
        solution = f"\n{(series['n'] / 2) * (2 * (series['a'] + series['b']) + (series['n'] - 1) * series['a'])}"
        generate_picture(series['rule'],
                         f"\nBereken die som van die volgende reeks tot en met die {series['n']}'de term:")

        return problem, solution

    @staticmethod
    def arithmetic_find_term_problem():
        seq = _gen_arithmetic_sequence()
        problem = f"\nIn die ry met die reel, ${seq['rule']}$, \nwatse term is gelyk aan {seq['Tn']}?"
        solution = f"\nn = {seq['n']}"
        generate_picture("", problem)
        return problem, solution

    @staticmethod
    def arithmetic_first_five_terms_problem():
        seq = _gen_arithmetic_sequence()
        problem = f"\nWat is die eerste 5 terme van 'n ry waar {seq['rule']}?"
        solution = seq['First_terms']
        generate_picture(seq['rule'], f"\nWat is die eerste 5 terme van 'n ry waar:")
        return problem, solution

    @staticmethod
    def arithmetic_sequence_rule_problem():
        seq = _gen_arithmetic_sequence()
        problem = f"\nVir die ry: ${seq['First_terms']}$\nWat is die algemene reel vir die ry?"
        solution = f"\n${seq['rule']}$"
        generate_picture("", f"\nVir die ry: ${seq['First_terms']}$\nWat is die algemene reel vir die ry?")
        return problem, solution

    @staticmethod
    def values_for_convergence_problem():
        a, b, c, r1, r2 = _gen_factored_quadratic()
        r1 = _random_non_zero(-10, 10)
        r2 = _random_non_zero(-10, 10)
        r = f"{_prettify_number(r1)}t {_prettify_number(r2)}".strip("+")
        t1 = f"{_prettify_number(a)}t^2 {_prettify_number(b)}t {_prettify_number(c)}".strip("+")
        a1 = a * r1
        b1 = (a * r2) + (r1 * b)
        c1 = (b * r2) + (c * r1)
        d1 = c * r2
        t2 = f"{_prettify_number(a1)}t^3 {_prettify_number(b1)}t^2 {_prettify_number(c1)}t {_prettify_number(d1)}".strip(
            "+")

        problem = f"\nDit word gegee dat die eerste twee terme van die reeks gelyk is aan: {t1}; {t2}\n\n" \
                  f"Vir watter waardes van t sal die meetkundige reeks konvergeer."
        solution = f"\nEerstens, vind die gemeenskaplike verhouding r = {r}" \
                   f"\nStel dan die ongelykheid op waar $-1<{r}<1$" \
                   f"\nDie finale antwoord is ${(-1 - r2) / r1}<t<{(1 - r2) / r1}$"

        generate_picture(f"{t1}; {t2}",
                         "\nVir watter waardes van t sal die meetkundige reeks konvergeer. "
                         "Dit word gegee dat die eerste twee terme van die reeks gelyk is aan:")

        return problem, solution

    @staticmethod
    def geometric_ratio_problem():
        a = _random_non_zero(-10, 10)
        r = _random_non_zero(-6, 7)
        n = _random_non_zero(5, 8)
        tn = a * (r ** (n - 1))

        if r < 0:
            positive_or_negative = "negatiewe"
        else:
            positive_or_negative = "positiewe"

        problem = f"\nBereken die verhouding van 'n meetkundige ry \nwaar term 1 gelyk is aan {a} en term {n} gelyk" \
                  f" is aan {tn}\n (r is 'n {positive_or_negative} heelgetal)"
        solution = f"\nStel die vergelyking op $a.r^{{(n-1)}} = tn$\n vervang waardes: ${a}.r^{{({n}-1)}} = {tn}$\nLos op vir r: " \
                   f"$r^{{({n - 1})}} = {tn}/{a}$\n $r = \\sqrt[{n - 1}]{{{tn / a}}}$\n $r = {r}$ is die verhouding vir die " \
                   f"gegewe meetkundige reeks "
        generate_picture("", problem)

        return problem, solution


##################################################################
# Generate questions


topics_and_problems = \
    [
        ["Algebra",
         [
             "factored_quadratic_problem", "unfactored_quadratic_problem", "quadratic_inequality_problem",
             "rooted_quadratic_problem", "simultaneous_equation_problem"
         ]
         ],
        ["Calculus",
         [
             "first_principles_problem", "derivative_problem", "minimum_gradient_problem"
         ]
         ],
        ["Finance",
         [
             "unknown_interest_problem", "annuity_will_he_make_it_problem", "delayed_car_payment_loan"
         ]
         ],
        ["Functions",
         [
             "hyperbola_unknown_p_and_q_problem", "hyperbola_x_intercept_problem", "new_parabola_from_old_problem",
             "hyperbola_axis_of_symmetry_problem", "hyperbola_inequality_question", "para_expo_c_problem",
             "para_expo_d_problem", "para_expo_b_and_q_problem", "para_expo_g_range_problem",
             "adding_k_to_f_problem", "linear_inverse_c_problem", "linear_inverse_equation_problem",
             "linear_inverse_a_coordinate_problem", "linear_inverse_ab_length_problem",
             "linear_inverse_area_problem", "unknown_parabola"
         ]
         ],
        ["Probability",
         [
             "event_not_occurring_problem", "abc_intersection_problem", "determine_at_least_two_events_problem",
             "are_events_independent", "combination_problem", "another_combination_problem"
         ]
         ],
        ["SequencesAndSeries",
         [
             "quadratic_unknown_rule_problem", "quadratic_unknown_tn_problem",
             "quadratic_unknown_n_problem", "quadratic_first_difference_sum_proof_problem",
             "geometric_unknown_rule_problem",
             "geometric_unknown_tn_problem", "geometric_unknown_n_problem", "geometric_list_first_terms_problem",
             "geometric_infinity_problem", "sigma_expansion_problem", "rewrite_to_sigma_problem",
             "arithmetic_series_to_n_problem", "arithmetic_find_term_problem", "arithmetic_first_five_terms_problem",
             "arithmetic_sequence_rule_problem", "values_for_convergence_problem", "geometric_ratio_problem",
             "geometric_series_ratio_problem"
         ]
         ]
    ]


def generate_question(current_topic_no, current_sub_topic_no):
    # Choose a random topic
    # current_topic_selector = random.randint(0, len(topic_list)-1)
    # current_topic = topic_list[current_topic_selector][0]
    # current_sub_topics = topic_list[current_topic_selector][1]
    # current_sub_topic = current_sub_topics[random.randint(0, len(current_sub_topics)-1)]
    # Instantiate the class dynamically
    current_topic_object = topics_and_problems[current_topic_no]
    current_topic = current_topic_object[0]
    current_sub_topic = current_topic_object[1][current_sub_topic_no]

    question_class = globals()[current_topic]
    question_instance = question_class(current_sub_topic)
    problem, solution = question_instance.get_problem_and_solution()
    # question generated
    print("question generated")

    return problem, solution


def get_checklist(current_topic_no, current_sub_topic_no):
    checklist_list = \
        [
            [
                "Algebra",
                [
                    [
                        ["Has the student set the equation equal to 0 ie moved all terms to one side before factoring?"],
                        ["Has the student started with the correct equation?"],
                        ["Has the student factored correctly?"],
                        ["Has the student solved correctly after factoring?"]
                    ],
                    [
                        ["Has the student used the correct formula? (The quadratic formula)"],
                        ["Has the student used the correct value for a in the formula?"],
                        ["Has the student used the correct value for b in the formula?"],
                        ["Has the student used the correct value for c in the formula?"],
                        ["Has the student solved the formula correctly?"]
                    ],
                    [
                        ["Did the student start with the correct problem?"],
                        ["Has the student succesfully obtained the critical values for the inequality?"],
                        ["Has the student correctly identified the regions in which the given expression"
                         " would be positive or negative?"],
                        ["has the student used the correct operators in his final expression of his answer?"]
                    ],
                    [
                        ["Has the student set the equation equal to 0 ie moved "
                         "all terms to one side before factoring?"],
                        ["Has the student started with the correct equation?"],
                        ["Has the student factored correctly?"],
                        ["Has the student solved correctly after factoring?"]
                    ],
                    []
                ]
            ],
            [
                "Calculus",
                [
                    [
                        ["Did the student use the correct formula for first principles derivation?", [0]],
                        ["Did the student calculate f(x + h) correctly?", [1]],
                        ["Did the student attempt to find the derivative of the correct function?"],
                        ["Did the student get rid of the h at the "
                         "denominator of the fraction by factoring and elimination before evaluating the limit?"],
                        ["Did the student correctly evaluate the limit?"[-2]],
                        ["Did the student correctly express his final answer? (Based on his own working)"]
                    ],
                    [
                        ["Did the student correctly subtract 1 from all powers of x?"],
                        ["Did the student correctly multiply the powers of x to the coefficients of x?"],
                        ["Did the student correctly express his final answer?"]
                    ],
                    [
                        ["Did the student correctly calculate g'(x)", [1]],
                        ["Did the student correctly calculate g''(x)", [2]],
                        ["Did the student set g''(x) = 0 at x's turning point.", [3]],
                        ["Did the student correctly solve for a?", [4, 5, 6]],
                        ["Did the student correctly set g''(x) < 0 or g''(x) > 0?", [7]],
                        ["Did the student solve the rest of the inequality correctly?", [8, 9, 10, 11]]
                    ]
                ]
            ],
            [
                "Finance",
                [
                    [
                        ["Did the student use the correct formula for accumulating the compounded interest?"],
                        ["Did the student use the correct values for a, p and n?"],
                        ["Did the student use the correct interest rate time preiod? (ie interest compounded monthly,"
                         " quarterly, annually or bi-annually?)"],
                        ["Did the student solve the equation correctly?"]
                    ],
                    [
                        ["Did the student use the correct formula? (Future value annuity formula?)"],
                        ["Did the user use the correct values for x, i and n?"],
                        ["Did the student compound the interest correctly?"],
                        ["Did the student solve the equation correctly?"],
                        ["Did the student compare the future value of the annuity to the item price?"]
                    ],
                    [
                        ["Did the student correctly calculate the deposit?"],
                        ["Did the student correctly calculate the amount of the loan?"],
                        ["Did the student add interest in the months preceding the first payment, after the"
                         " loan was initiated"],
                        ["Did the student use the correct formula to calculate the repayment?"
                         " (present value annuity formula)"],
                        ["Did the student use the correct values for p, i and n in the formula?"],
                        ["Was the student's interest rate compounded correctly?"],
                        ["Did the student solve the equation correctly?"]
                    ]
                ]
            ],
            [
                "Functions",
                [
                    [
                        ["Did the student remember to change the sign of the vertical asimptote? "
                         "(If the asimptote is positive the value of p is negative and vice versa)"]
                    ],
                    [
                        ["Did the student set y = 0 to solve for the x-intercept?"]
                    ],
                    [
                        ["Did the student calculate g(x) correctly?"],
                        ["Did the student set g(x) = 0 to solve for the x-intercept?"],
                        ["Did the student solve the equation correctly?"]
                    ],
                    [
                        ["Did the student sub in the point of intersection of the asymptotes"
                         " to get the axis of symmetry?"]
                    ],
                    [
                        ["What do you think the student did wrong?"]
                    ],
                    [
                        [""]
                    ],
                    [
                        ["Did the student find the coordinate of d by finding the turning point of f(x)?"]
                    ],
                    [
                        ["Did the student correctly set q = the c value of f(x)?"],
                        ["Did the student sorrectly sub in point D into the equation to solve for b?"]
                    ],
                    [
                        [""]
                    ],
                    [
                        [""]
                    ],
                    [
                        [""]
                    ],
                    [
                        ["Did the student swop the x and y values of the original function?"],
                        ["Did the student solve the equation correctly?"]
                    ],
                    [
                        ["Did the student set g(x) = g^(-1)(x)"],
                        ["Did the student solve correctly for x?"],
                        ["Did the student use the x value that was calculated to solve for y?"]
                    ],
                    [
                        ["Did the student correctly get the coordinates of A?"],
                        ["Did the student correctly get the coordinates of B?"],
                        ["Did the student use the distance formula? (between points a and b?)"],
                        ["Did the student correctly solve the distance formula?"]
                    ],
                    [
                        [""]
                    ],
                    [
                        [""]
                    ]
                ]
            ],
            [
                "Probability",
                [

                ]
            ]
        ]
    try:
        return checklist_list[current_topic_no][1][current_sub_topic_no]
    except IndexError:
        return None


