import re
import sympy as sp
from typing import Dict, List, Any
from models.schemas import ExplanationLevel, LearningProfile
from services.gemini_service import GeminiService

class MathParser:
    def __init__(self):
        # Initialize Gemini service for enhanced math explanations
        self.gemini_service = GeminiService()
        
        # Common math symbols and their LaTeX representations
        self.math_symbols = {
            '+': 'plus',
            '-': 'minus',
            '*': 'times',
            '/': 'divided by',
            '=': 'equals',
            '^': 'to the power of',
            'sqrt': 'square root of',
            'pi': 'pi',
            'sin': 'sine of',
            'cos': 'cosine of',
            'tan': 'tangent of'
        }
        
        # Initialize SymPy symbols
        self.x, self.y, self.z = sp.symbols('x y z')
        self.a, self.b, self.c = sp.symbols('a b c')
    
    def parse_and_solve(self, math_expression: str, explanation_level: ExplanationLevel = ExplanationLevel.INTERMEDIATE) -> Dict[str, Any]:
        """
        Task 7: Math Parsing & Dyscalculia Support
        Parse math expressions and generate step-by-step explanations
        """
        try:
            # Clean and parse the expression
            cleaned_expression = self._clean_expression(math_expression)
            
            # Determine the type of problem
            problem_type = self._classify_problem(cleaned_expression)
            
            # Generate solution steps
            steps = self._generate_solution_steps(cleaned_expression, problem_type, explanation_level)
            
            # Try to enhance explanations with Gemini
            if steps:
                # Determine learning profile based on explanation level
                profile = LearningProfile.DYSCALCULIA if explanation_level == ExplanationLevel.BASIC else LearningProfile.NEUROTYPICAL
                enhanced_steps = self.gemini_service.generate_math_explanation(math_expression, steps, profile)
                if enhanced_steps:
                    steps = enhanced_steps
            
            # Get final answer
            final_answer = self._get_final_answer(cleaned_expression)
            
            # Determine difficulty level
            difficulty_level = self._assess_difficulty(cleaned_expression, problem_type)
            
            return {
                "problem": math_expression,
                "steps": steps,
                "final_answer": final_answer,
                "difficulty_level": difficulty_level
            }
            
        except Exception as e:
            raise Exception(f"Math parsing failed: {str(e)}")
    
    def _clean_expression(self, expression: str) -> str:
        """Clean and standardize math expression"""
        # Remove extra whitespace
        expression = ' '.join(expression.split())
        
        # Replace common math notations
        replacements = {
            '×': '*',
            '÷': '/',
            '²': '**2',
            '³': '**3',
            '√': 'sqrt',
            'π': 'pi',
            '∞': 'oo'
        }
        
        for old, new in replacements.items():
            expression = expression.replace(old, new)
        
        # Handle implicit multiplication (e.g., 2x -> 2*x)
        expression = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', expression)
        expression = re.sub(r'([a-zA-Z])(\d+)', r'\1*\2', expression)
        
        return expression
    
    def _classify_problem(self, expression: str) -> str:
        """Classify the type of mathematical problem"""
        if '=' in expression:
            if '^' in expression or '**' in expression:
                return "quadratic_equation"
            elif any(op in expression for op in ['sin', 'cos', 'tan', 'log']):
                return "trigonometric_equation"
            else:
                return "linear_equation"
        elif any(op in expression for op in ['sin', 'cos', 'tan']):
            return "trigonometric_expression"
        elif '^' in expression or '**' in expression:
            return "polynomial_expression"
        elif '/' in expression:
            return "fraction_expression"
        else:
            return "arithmetic_expression"
    
    def _generate_solution_steps(self, expression: str, problem_type: str, explanation_level: ExplanationLevel) -> List[Dict[str, Any]]:
        """Generate step-by-step solution"""
        steps = []
        
        try:
            if problem_type == "linear_equation":
                steps = self._solve_linear_equation(expression, explanation_level)
            elif problem_type == "quadratic_equation":
                steps = self._solve_quadratic_equation(expression, explanation_level)
            elif problem_type == "arithmetic_expression":
                steps = self._solve_arithmetic_expression(expression, explanation_level)
            elif problem_type == "fraction_expression":
                steps = self._solve_fraction_expression(expression, explanation_level)
            else:
                steps = self._solve_general_expression(expression, explanation_level)
                
        except Exception as e:
            # Fallback to basic explanation
            steps = [{
                "step_number": 1,
                "explanation": f"This is a {problem_type.replace('_', ' ')} problem.",
                "intermediate_result": expression
            }]
        
        return steps
    
    def _solve_linear_equation(self, expression: str, explanation_level: ExplanationLevel) -> List[Dict[str, Any]]:
        """Solve linear equation step by step"""
        steps = []
        
        # Parse the equation
        if '=' in expression:
            left_side, right_side = expression.split('=', 1)
            
            # Step 1: Identify the equation
            steps.append({
                "step_number": 1,
                "explanation": "This is a linear equation. We need to solve for the variable.",
                "intermediate_result": f"{left_side} = {right_side}"
            })
            
            # Step 2: Move all terms to one side
            try:
                # Use SymPy to solve
                eq = sp.Eq(sp.sympify(left_side), sp.sympify(right_side))
                solution = sp.solve(eq, self.x)
                
                if solution:
                    steps.append({
                        "step_number": 2,
                        "explanation": "Solving the equation using algebraic methods.",
                        "intermediate_result": f"x = {solution[0]}"
                    })
                else:
                    steps.append({
                        "step_number": 2,
                        "explanation": "The equation has no solution or infinite solutions.",
                        "intermediate_result": "No unique solution"
                    })
                    
            except Exception:
                steps.append({
                    "step_number": 2,
                    "explanation": "This equation requires algebraic manipulation to solve.",
                    "intermediate_result": "Solution requires further steps"
                })
        
        return steps
    
    def _solve_quadratic_equation(self, expression: str, explanation_level: ExplanationLevel) -> List[Dict[str, Any]]:
        """Solve quadratic equation step by step"""
        steps = []
        
        if '=' in expression:
            left_side, right_side = expression.split('=', 1)
            
            steps.append({
                "step_number": 1,
                "explanation": "This is a quadratic equation. We can solve it using the quadratic formula.",
                "intermediate_result": f"{left_side} = {right_side}"
            })
            
            try:
                # Use SymPy to solve
                eq = sp.Eq(sp.sympify(left_side), sp.sympify(right_side))
                solutions = sp.solve(eq, self.x)
                
                if solutions:
                    if len(solutions) == 1:
                        steps.append({
                            "step_number": 2,
                            "explanation": "The quadratic equation has one real solution.",
                            "intermediate_result": f"x = {solutions[0]}"
                        })
                    else:
                        steps.append({
                            "step_number": 2,
                            "explanation": "The quadratic equation has two solutions.",
                            "intermediate_result": f"x = {solutions[0]} or x = {solutions[1]}"
                        })
                else:
                    steps.append({
                        "step_number": 2,
                        "explanation": "The quadratic equation has no real solutions.",
                        "intermediate_result": "No real solutions"
                    })
                    
            except Exception:
                steps.append({
                    "step_number": 2,
                    "explanation": "This quadratic equation can be solved using factoring or the quadratic formula.",
                    "intermediate_result": "Use quadratic formula: x = (-b ± √(b² - 4ac)) / 2a"
                })
        
        return steps
    
    def _solve_arithmetic_expression(self, expression: str, explanation_level: ExplanationLevel) -> List[Dict[str, Any]]:
        """Solve arithmetic expression step by step"""
        steps = []
        
        steps.append({
            "step_number": 1,
            "explanation": "This is an arithmetic expression. We need to follow the order of operations.",
            "intermediate_result": expression
        })
        
        try:
            # Use SymPy to evaluate
            result = sp.sympify(expression)
            simplified = sp.simplify(result)
            
            steps.append({
                "step_number": 2,
                "explanation": "Simplifying the expression using order of operations.",
                "intermediate_result": str(simplified)
            })
            
            # If it's a number, calculate the final value
            if simplified.is_number:
                steps.append({
                    "step_number": 3,
                    "explanation": "Calculating the final numerical result.",
                    "intermediate_result": str(float(simplified))
                })
                
        except Exception:
            steps.append({
                "step_number": 2,
                "explanation": "This expression can be simplified using arithmetic rules.",
                "intermediate_result": "Simplified form"
            })
        
        return steps
    
    def _solve_fraction_expression(self, expression: str, explanation_level: ExplanationLevel) -> List[Dict[str, Any]]:
        """Solve fraction expression step by step"""
        steps = []
        
        steps.append({
            "step_number": 1,
            "explanation": "This is a fraction expression. We need to simplify it.",
            "intermediate_result": expression
        })
        
        try:
            # Use SymPy to simplify fractions
            result = sp.sympify(expression)
            simplified = sp.simplify(result)
            
            steps.append({
                "step_number": 2,
                "explanation": "Simplifying the fraction by finding common factors.",
                "intermediate_result": str(simplified)
            })
            
        except Exception:
            steps.append({
                "step_number": 2,
                "explanation": "This fraction can be simplified by finding the greatest common divisor.",
                "intermediate_result": "Simplified fraction"
            })
        
        return steps
    
    def _solve_general_expression(self, expression: str, explanation_level: ExplanationLevel) -> List[Dict[str, Any]]:
        """Solve general mathematical expression"""
        steps = []
        
        steps.append({
            "step_number": 1,
            "explanation": "This is a mathematical expression that needs to be simplified.",
            "intermediate_result": expression
        })
        
        try:
            result = sp.sympify(expression)
            simplified = sp.simplify(result)
            
            steps.append({
                "step_number": 2,
                "explanation": "Simplifying the expression using mathematical rules.",
                "intermediate_result": str(simplified)
            })
            
        except Exception:
            steps.append({
                "step_number": 2,
                "explanation": "This expression can be simplified using mathematical properties.",
                "intermediate_result": "Simplified form"
            })
        
        return steps
    
    def _get_final_answer(self, expression: str) -> str:
        """Get the final answer for the mathematical expression"""
        try:
            result = sp.sympify(expression)
            simplified = sp.simplify(result)
            
            if simplified.is_number:
                return str(float(simplified))
            else:
                return str(simplified)
                
        except Exception:
            return "Solution requires further steps"
    
    def _assess_difficulty(self, expression: str, problem_type: str) -> str:
        """Assess the difficulty level of the mathematical problem"""
        # Count variables
        variables = len(re.findall(r'[a-zA-Z]', expression))
        
        # Count operations
        operations = len(re.findall(r'[+\-*/^]', expression))
        
        # Check for special functions
        special_functions = len(re.findall(r'(sin|cos|tan|log|sqrt)', expression))
        
        # Determine difficulty based on complexity
        if special_functions > 0 or problem_type == "quadratic_equation":
            return "hard"
        elif variables > 1 or operations > 3:
            return "medium"
        else:
            return "easy"
    
    def explain_step_in_plain_english(self, step: Dict[str, Any]) -> str:
        """Convert mathematical step to plain English explanation"""
        explanation = step["explanation"]
        
        # Replace mathematical symbols with words
        for symbol, word in self.math_symbols.items():
            explanation = explanation.replace(symbol, word)
        
        return explanation
