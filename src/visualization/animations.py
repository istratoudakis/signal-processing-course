# Libraries
import os
from manim import *

# 1080p configuration
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60
config.verbosity = "WARNING"
os.environ["MANIM_CONFIG_VERBOSITY"] = "WARNING"

# 2. SCENE DEFINITION
class PolynomialCalibrationModel(Scene):
    def construct(self):
        # Coordinate Axes setup
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 8, 2],
            x_length=8,
            y_length=4.5,  
            axis_config={"include_numbers": True, "tip_shape": StealthTip},
        ).to_edge(DOWN, buff=0.4)
        
        x_label = axes.get_x_axis_label(Tex(r"T ($^\circ\text{C}$)").scale(0.7), edge=RIGHT, direction=DOWN)
        y_label = axes.get_y_axis_label(Tex(r"y (\text{V})").scale(0.7), edge=UP, direction=LEFT)

        # Title and mathematical formula setup
        title = Title("Step-by-Step Construction of the Sensor Response", include_underline=False).scale(0.75).to_edge(UP, buff=0.3)
        
        formula = MathTex(
            r"y(T) = ", r"\theta_0", r" + ", r"\theta_1 T", r" + ", r"\theta_2 T^2"
        ).scale(0.8).next_to(title, DOWN, buff=0.2)

        # Intro: render title, formula, and coordinate frame
        self.play(Write(title))
        self.play(Write(formula))
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(1)

        # Fade out main title to optimize vertical canvas space
        # Reposition the formula to the very top edge
        self.play(
            FadeOut(title),
            formula.animate.to_edge(UP, buff=0.4),
            run_time=1.2
        )
        self.wait(0.5)

        # Step 1: Baseline constant offset θ0
        c0 = 1.0
        curve_offset = axes.plot(lambda t: c0, x_range=[0, 100], color=GRAY)
        self.play(
            formula[1].animate.set_color(GRAY),
            Create(curve_offset),
            run_time=1.5
        )
        self.wait(1)

        # Step 2: Superposition of linear sensitivity θ1
        c1 = 0.03
        curve_linear = axes.plot(lambda t: c0 + c1 * t, x_range=[0, 100], color=BLUE)
        self.play(
            formula[3].animate.set_color(BLUE),
            Transform(curve_offset, curve_linear),
            run_time=1.5
        )
        self.wait(1)

        # Step 3: Superposition of quadratic nonlinearity θ2
        c2 = 0.0004
        curve_full = axes.plot(lambda t: c0 + c1 * t + c2 * (t**2), x_range=[0, 100], color=YELLOW)
        self.play(
            formula[5].animate.set_color(YELLOW),
            Transform(curve_offset, curve_full),
            run_time=1.5
        )
        self.wait(2)
        
        # Outro: smoothly fade out the formula, leaving the synthesized calibration curve
        self.play(FadeOut(formula), run_time=1)
        self.wait(1)

class WhiteningGeometry(ThreeDScene):
    def construct(self):
        grid = NumberPlane(
            x_range=[-1, 8, 1], y_range=[-1, 8, 1],
            background_line_style={"stroke_color": TEAL, "stroke_width": 1, "stroke_opacity": 0.5}
        )
        self.play(Create(grid), run_time=1.5)
        
        # Proper way to fix text in frame for 3D scenes
        title = Title("Geometry of WLS: The Whitening Transformation", font_size=36, include_underline=False).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        x_vec = np.array([2.0, 1.0, 0.0])  
        y_vec = np.array([1.5, 4.0, 0.0])  
        
        cx_line = Line(grid.c2p(-2, -1), grid.c2p(8, 4), color=WHITE, stroke_width=2)
        cx_label = MathTex(r"\mathcal{C}(X)").move_to(grid.c2p(6.5, 3.8)) 
        
        vec_y = Arrow(grid.c2p(0, 0), grid.c2p(*y_vec[:2]), buff=0, color=YELLOW, max_tip_length_to_length_ratio=0.1)
        label_y = MathTex("y").next_to(vec_y.get_end(), UP)
        
        self.play(Create(cx_line), Write(cx_label))
        self.play(GrowArrow(vec_y), Write(label_y))
        self.wait(1)

        # --- OLS PROJECTION ---
        y_hat_ols = 1.4 * x_vec
        vec_y_ols = Arrow(grid.c2p(0, 0), grid.c2p(*y_hat_ols[:2]), buff=0, color=RED)
        residual_ols = DashedLine(grid.c2p(*y_hat_ols[:2]), grid.c2p(*y_vec[:2]), color=RED)
        
        ra_ols = RightAngle(
            Line(grid.c2p(0, 0), grid.c2p(*y_hat_ols[:2])), 
            Line(grid.c2p(*y_hat_ols[:2]), grid.c2p(*y_vec[:2])), 
            length=0.25, color=RED
        )
        
        text_ols = Tex("OLS: Orthogonal in Euclidean Space", color=RED, font_size=30).to_corner(DR)
        self.add_fixed_in_frame_mobjects(text_ols)
        
        self.play(Write(text_ols))
        self.play(GrowArrow(vec_y_ols), Create(residual_ols))
        self.play(Create(ra_ols))
        self.wait(2)
        
        self.play(FadeOut(vec_y_ols), FadeOut(residual_ols), FadeOut(ra_ols), FadeOut(text_ols))

        # --- WLS PROJECTION ---
        alpha_wls = 14.0 / 16.5
        y_hat_wls = alpha_wls * x_vec
        vec_y_wls = Arrow(grid.c2p(0, 0), grid.c2p(*y_hat_wls[:2]), buff=0, color=BLUE)
        residual_wls = DashedLine(grid.c2p(*y_hat_wls[:2]), grid.c2p(*y_vec[:2]), color=BLUE)
        
        text_wls = Tex("WLS: Not visibly orthogonal in standard space...", color=BLUE, font_size=30).to_corner(DR)
        self.add_fixed_in_frame_mobjects(text_wls)
        
        self.play(Write(text_wls))
        self.play(GrowArrow(vec_y_wls), Create(residual_wls))
        self.wait(2)

        # --- WHITENING TRANSFORMATION & 3D ROTATION ---
        text_transform = Tex(r"Applying Whitening: $\tilde{X} = \sqrt{W} X, \quad \tilde{y} = \sqrt{W} y$", color=GREEN, font_size=30).to_corner(DR)
        self.add_fixed_in_frame_mobjects(text_transform)
        
        self.play(ReplacementTransform(text_wls, text_transform), FadeOut(cx_label), FadeOut(label_y))
        
        # Rotate the camera to view the plane from an angle (3D Magic)
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, run_time=2.5)
        
        # Apply the transformation (3x3 matrix for 3D compatibility)
        matrix = [[2.0, 0.0, 0.0], [0.0, np.sqrt(0.5), 0.0], [0.0, 0.0, 1.0]]
        transformable_group = VGroup(grid, cx_line, vec_y, vec_y_wls, residual_wls)
        
        self.play(transformable_group.animate.apply_matrix(matrix), run_time=3, rate_func=smooth)
        self.wait(1)

        # --- REVEAL EXACT ORTHOGONALITY ---
        origin_pt = grid.c2p(0, 0)
        wls_end_pt = vec_y_wls.get_end()
        y_end_pt = vec_y.get_end()
        
        ra_wls = RightAngle(
            Line(origin_pt, wls_end_pt), Line(wls_end_pt, y_end_pt), 
            length=0.25, color=GREEN
        )
        
        text_final = Tex(r"WLS is an exact Orthogonal Projection in $\mathcal{C}(\tilde{X})$!", color=GREEN, font_size=30).to_corner(DR)
        self.add_fixed_in_frame_mobjects(text_final)
        
        self.play(ReplacementTransform(text_transform, text_final))
        self.play(Create(ra_wls))
        
        # Slow cinematic camera pan at the end
        self.move_camera(theta=-15 * DEGREES, run_time=4)
        self.wait(1)

class ExtrapolationIllusion(Scene):
    def construct(self):
        # --- SCENE 1: The Narrow Window (25.0 to 25.2) ---
        axes_narrow = Axes(
            x_range=[24.9, 25.3, 0.1],
            y_range=[1.95, 2.05, 0.05],
            x_length=10,
            y_length=5.5,
            axis_config={"include_numbers": True, "font_size": 28, "tip_shape": StealthTip}
        ).to_edge(DOWN, buff=0.6)
        
        x_label_n = axes_narrow.get_x_axis_label(Tex(r"T ($^\circ\text{C}$)", font_size=32), edge=RIGHT, direction=UP, buff=0.2)
        y_label_n = axes_narrow.get_y_axis_label(Tex(r"y (\text{V})", font_size=32), edge=UP, direction=RIGHT, buff=0.2)
        
        title_narrow = Title(
            "Narrow Window: Both OLS and Stabilized Fit Appear Accurate",
            color=WHITE, font_size=34
        ).to_edge(UP, buff=0.2)
        
        self.play(Create(axes_narrow), Write(x_label_n), Write(y_label_n), Write(title_narrow))

        # 1. Generate synthetic noisy data within [25.0, 25.2]
        np.random.seed(42)
        t_vals = np.linspace(25.0, 25.2, 8)
        y_vals = 1.0 + 0.03 * t_vals + 0.0004 * (t_vals**2) + np.random.normal(0, 0.001, 8)
        dots = VGroup(*[Dot(axes_narrow.c2p(t, y), color=WHITE, radius=0.07) for t, y in zip(t_vals, y_vals)])
        
        self.play(FadeIn(dots))

        # 2. Compute standard OLS and Augmented Tikhonov solution mathematically
        X_ols = np.column_stack([np.ones_like(t_vals), t_vals, t_vals**2])
        theta_ols, *_ = np.linalg.lstsq(X_ols, y_vals, rcond=None)

        L = np.diag([0, 1, 1])
        lam = 1e-4
        X_aug = np.vstack([X_ols, np.sqrt(lam) * L])
        y_aug = np.concatenate([y_vals, np.zeros(3)])
        theta_aug, *_ = np.linalg.lstsq(X_aug, y_aug, rcond=None)

        def ols_func(t): return theta_ols[0] + theta_ols[1]*t + theta_ols[2]*(t**2)
        def aug_func(t): return theta_aug[0] + theta_aug[1]*t + theta_aug[2]*(t**2)

        # 3. Plot both curves in the narrow window to show they nearly overlap
        curve_ols_narrow = axes_narrow.plot(ols_func, x_range=[24.92, 25.28], color=RED, stroke_width=4)
        curve_aug_narrow = DashedVMobject(
            axes_narrow.plot(aug_func, x_range=[24.92, 25.28], color=GREEN, stroke_width=4),
            num_dashes=35
        )
        
        ols_label_n = Tex("Standard OLS", color=RED, font_size=32).move_to(axes_narrow.c2p(25.05, 2.025))
        aug_label_n = Tex("Stabilized (Augmented)", color=GREEN, font_size=32).move_to(axes_narrow.c2p(25.18, 1.98))
        
        self.play(Create(curve_ols_narrow), Write(ols_label_n), run_time=1.5)
        self.wait(0.5)
        self.play(Create(curve_aug_narrow), Write(aug_label_n), run_time=1.5)
        self.wait(2)

        # --- SCENE 2: The Zoom-Out (0 to 50) ---
        # Y-range tailored to [0, 18] so the upward parabola divergence fills the frame cleanly
        axes_wide = Axes(
            x_range=[0, 50, 10],
            y_range=[0, 18, 3],
            x_length=10,
            y_length=5.5,
            axis_config={"include_numbers": True, "font_size": 28, "tip_shape": StealthTip}
        ).to_edge(DOWN, buff=0.6)
        
        x_label_w = axes_wide.get_x_axis_label(Tex(r"T ($^\circ\text{C}$)", font_size=32), edge=RIGHT, direction=UP, buff=0.2)
        y_label_w = axes_wide.get_y_axis_label(Tex(r"y (\text{V})", font_size=32), edge=UP, direction=RIGHT, buff=0.2)
        
        title_wide = Title(
            "The Zoom-Out: OLS Wild Extrapolation vs Stabilized Augmented System",
            color=WHITE, font_size=34
        ).to_edge(UP, buff=0.2)
        
        # Redraw curves on the wide coordinate system
        curve_ols_wide = axes_wide.plot(ols_func, x_range=[0, 50], color=RED, stroke_width=4)
        curve_aug_wide = axes_wide.plot(aug_func, x_range=[0, 50], color=GREEN, stroke_width=4)
        
        dots_wide = VGroup(*[Dot(axes_wide.c2p(t, y), color=YELLOW, radius=0.05) for t, y in zip(t_vals, y_vals)])

        # Cinematic Zoom-Out Transition (both curves transform simultaneously)
        self.play(
            Transform(axes_narrow, axes_wide),
            Transform(x_label_n, x_label_w),
            Transform(y_label_n, y_label_w),
            Transform(title_narrow, title_wide),
            Transform(curve_ols_narrow, curve_ols_wide),
            Transform(curve_aug_narrow, curve_aug_wide),
            Transform(dots, dots_wide),
            FadeOut(ols_label_n),
            FadeOut(aug_label_n),
            run_time=3.5,
            rate_func=smooth
        )
        self.wait(0.5)

        # Clean, non-overlapping annotations in the wide view
        warning_text = Tex("OLS diverges dramatically outside window!", color=RED, font_size=30).move_to(axes_wide.c2p(25, 13.5))
        stable_label = Tex("Stabilized Curve (Augmented System)", color=GREEN, font_size=30).move_to(axes_wide.c2p(32, 4.8))
        
        self.play(Write(warning_text), Write(stable_label))
        self.wait(3)