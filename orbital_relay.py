import customtkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import json


class RelayNetworkPlanner:
    def __init__(self):
        self._load_data()
        self._build_window()
        self._build_figure()
        self._build_controls()
        self.update_plot()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    # ----- Initialization -----
    def _load_data(self):
        with open("celestial_bodies.json", "r", encoding="utf-8") as f:
            self.celestial_bodies = json.load(f)
        with open("antennas.json", "r", encoding="utf-8") as f:
            self.antennas = json.load(f)

    def _build_window(self):
        self.root = tk.CTk()
        self.root.title("KSP Relay Network Planner")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def _build_figure(self):
        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor("black")
        self.fig.subplots_adjust(left=0, right=1, top=0.9, bottom=0.05)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, sticky="nsew")

    def _build_controls(self):
        # ----- Variables -----
        self.body_var = tk.StringVar(value=list(self.celestial_bodies.keys())[4])
        self.relay_var = tk.StringVar(value=list(self.antennas.keys())[4])
        self.vessel_var = tk.StringVar(value=list(self.antennas.keys())[0])
        self.sats_var = tk.IntVar(value=3)
        self.antennas_var = tk.IntVar(value=2)
        self.signal_var = tk.DoubleVar(value=0.8)
        self.period_mode = tk.StringVar(value="Seconds")
        self.geo_mode = tk.BooleanVar(value=False)

        # ----- Control frame -----
        controls_frame = tk.CTkFrame(self.root)
        controls_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=10)
        controls_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Row 0 - Celestial body select
        tk.CTkLabel(controls_frame, text="Body").grid(row=0, column=0, sticky="e")
        tk.CTkOptionMenu(controls_frame, variable=self.body_var, values=list(self.celestial_bodies.keys()),
                         command=self.update_plot).grid(row=0, column=1, sticky="w", padx=10, pady=2)

        # Row 1 - Relay antenna select
        tk.CTkLabel(controls_frame, text="Relay Antenna").grid(row=1, column=0, sticky="e")
        tk.CTkOptionMenu(controls_frame, variable=self.relay_var, values=list(self.antennas.keys()),
                         command=self.update_plot).grid(row=1, column=1, sticky="w", padx=10, pady=2)

        # Row 2 - Vessel antenna select
        tk.CTkLabel(controls_frame, text="Vessel Antenna").grid(row=2, column=0, sticky="e")
        tk.CTkOptionMenu(controls_frame, variable=self.vessel_var, values=list(self.antennas.keys()),
                         command=self.update_plot).grid(row=2, column=1, sticky="w", padx=10, pady=2)

        # Row 3 - Satellite count slider
        tk.CTkLabel(controls_frame, text="Satellites").grid(row=3, column=0, sticky="e")
        tk.CTkSlider(controls_frame, from_=3, to=20, variable=self.sats_var,
                     command=self.update_plot).grid(row=3, column=1, sticky="ew", padx=10)
        self.sats_label = tk.CTkLabel(controls_frame, text="3")
        self.sats_label.grid(row=3, column=2, sticky="w")

        # Row 4 - Antenna count slider
        tk.CTkLabel(controls_frame, text="Antennas").grid(row=4, column=0, sticky="e")
        tk.CTkSlider(controls_frame, from_=1, to=20, variable=self.antennas_var,
                     command=self.update_plot).grid(row=4, column=1, sticky="ew", padx=10)
        self.antenna_label = tk.CTkLabel(controls_frame, text="2")
        self.antenna_label.grid(row=4, column=2, sticky="w")

        # Row 5 - Signal strength slider
        tk.CTkLabel(controls_frame, text="Minimum Signal Strength").grid(row=5, column=0, sticky="e")
        tk.CTkSlider(controls_frame, from_=.5, to=1.0, number_of_steps=50, variable=self.signal_var,
                     command=self.update_plot).grid(row=5, column=1, sticky="ew", padx=10)
        self.signal_label = tk.CTkLabel(controls_frame, text="80%")
        self.signal_label.grid(row=5, column=2, sticky="w")

        # Row 6 - Period precision
        tk.CTkLabel(controls_frame, text="Period Precision").grid(row=6, column=0, sticky="e")
        tk.CTkOptionMenu(controls_frame, variable=self.period_mode, values=["Seconds", "Minutes", "Hours"],
                         command=self.update_plot).grid(row=6, column=1, sticky="w", padx=10, pady=2)

        # Row 7 - Geostationary toggle
        tk.CTkLabel(controls_frame, text="Geostationary").grid(row=7, column=0, sticky="e")
        tk.CTkCheckBox(controls_frame, text="", variable=self.geo_mode,
                       command=self.update_plot).grid(row=7, column=1, sticky="w", padx=10)

        # ----- Messaging -----
        self.message_box = tk.CTkTextbox(self.root, height=130, width=400)
        self.message_box.grid(row=8, column=0, columnspan=4, padx=10, pady=10)
        self.message_box.configure(state="disabled")

    # ----- Update -----
    def update_plot(self, *args):
        body_name = self.body_var.get()
        relay_antenna = self.relay_var.get()
        vessel_antenna = self.vessel_var.get()
        n_sats = max(3, int(self.sats_var.get()))
        n_antennas = max(1, int(self.antennas_var.get()))
        target_signal = self.signal_var.get()
        geostationary = self.geo_mode.get()

        self.sats_label.configure(text=str(n_sats))
        self.antenna_label.configure(text=str(n_antennas))
        self.signal_label.configure(text=f"{int(target_signal * 100)}%")

        self._snap_slider(self.sats_var, 3)
        self._snap_slider(self.antennas_var, 1)

        messages = []

        # ----- Orbital information -----
        celestial_body = self.celestial_bodies[body_name]
        R_body = celestial_body["r_body"]               # Radius of the celestial body (km)
        mu = celestial_body["grav_param"]               # Standard gravitational parameter (m^3/s^2)
        soi_altitude = celestial_body["soi"]            # Sphere of influence radius (km)
        r_sync = celestial_body["sync_orbit_radius"]    # Geostationary orbit radius (km)
        use_sync = (r_sync > 0) and geostationary

        # ----- Antenna -----
        if not self.antennas[relay_antenna]["relay_capable"]:
            messages.append("⚠️ Satellite antenna is not relay capable!")

        P_relay = self.antennas[relay_antenna]["rating"]    # Power of the relay antenna
        P_vessel = self.antennas[vessel_antenna]["rating"]  # Power of the vessel's antenna

        # ----- Core Calculations -----
        P_combined = self.combined_power(P_relay, n_antennas)
        comm_range = np.floor(self.communication_range(P_combined, P_vessel))

        max_orbit_radius = np.floor(self.max_distance(comm_range, target_signal))
        max_altitude = max_orbit_radius - R_body

        geometric_minimum = self.minimum_altitude(R_body, n_sats)
        min_altitude = np.ceil(max(geometric_minimum, celestial_body["atmosphere_height"]))

        T_max = self.orbital_period(max_orbit_radius, mu)

        if use_sync:
            r_ideal = r_sync
            ideal_altitude = r_ideal - R_body
            T_ideal = self.orbital_period(r_ideal, mu)
            T_str = self.format_kerbal_time(T_ideal)

            if r_ideal > soi_altitude:
                messages.append("❌ Geostationary orbit lies outside SOI! This is impossible!")
            if ideal_altitude < min_altitude:
                messages.append("⚠️️ Geostationary orbit below minimum coverage altitude")
            if ideal_altitude > max_altitude:
                messages.append("⚠️ Signal strength insufficient for geostationary orbit with current parameters. Can't reach celestial body.")

        else:
            # ----- Ideal Orbit (period divisible by satellite count) -----
            # Default to second precision, then try to snap to coarser precision if requested
            T_ideal = np.floor(T_max / n_sats) * n_sats
            precision_multipliers = {"Minutes": 60, "Hours": 3600}
            precision_labels = {"Minutes": "Minute", "Hours": "Hour"}
            mode = self.period_mode.get()

            if mode in precision_multipliers:
                unit = n_sats * precision_multipliers[mode]
                candidate_T = np.floor(T_max / unit) * unit
                candidate_altitude = self.find_altitude_for_period(candidate_T, R_body, mu)

                if candidate_altitude < min_altitude:
                    messages.append(f"⚠️ {precision_labels[mode]} precision orbit falls below minimum altitude — falling back to seconds mode")
                else:
                    T_ideal = candidate_T

            T_str = self.format_kerbal_time(T_ideal)
            ideal_altitude = self.find_altitude_for_period(T_ideal, R_body, mu)
            r_ideal = R_body + ideal_altitude

        # ----- Phasing Orbits -----
        T_phase_high = ((n_sats + 1) / n_sats) * T_ideal
        T_phase_low = ((n_sats - 1) / n_sats) * T_ideal

        a_phase_high = ((T_phase_high / (2 * np.pi)) ** 2 * mu) ** (1 / 3) / 1000
        a_phase_low = ((T_phase_low / (2 * np.pi)) ** 2 * mu) ** (1 / 3) / 1000

        r_peri_low = 2 * a_phase_low - r_ideal
        r_peri_high = 2 * a_phase_high - r_ideal

        # ----- Create visualization -----
        orbit_messages = self._plot_full_network(
            T_str, body_name, min_altitude, max_altitude, ideal_altitude,
            r_peri_low, r_peri_high, n_sats, n_antennas, soi_altitude, use_sync
        )
        self._set_messages(messages + orbit_messages)
        self.canvas.draw()

    # ----- Plotting -----
    def _plot_full_network(self, T_str, body_name, h_min, h_max, h_ideal, r_phase_low, r_phase_high,
                           N, n_antennas, soi_altitude, is_sync):
        theta = np.linspace(0, 2 * np.pi, 1000)
        messages = []
        self.ax.clear()

        celestial_body = self.celestial_bodies[body_name]
        body_color = celestial_body["color"]
        body_radius = celestial_body["r_body"]
        h_atm = celestial_body["atmosphere_height"]
        label_offset = 0.05 * body_radius

        draw_sats = True
        draw_connection = True
        draw_apoapsis = True
        draw_apo_high = True
        draw_peri_low = True

        # ----- Radii (center-based) -----
        r_min = body_radius + h_min
        r_max = body_radius + h_max
        r_ideal = body_radius + h_ideal
        r_atm = body_radius + h_atm
        r_peri_low = r_phase_low
        r_apo_high = r_phase_high

        # ----- Helper drawing functions -----
        def draw_orbit(radius, style, label, color, width=1.5):
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            self.ax.plot(x, y, linestyle=style, color=color, linewidth=width, label=label)

        def draw_ellipse_from_focus(r_peri, r_apo, color, linestyle, label):
            a = (r_peri + r_apo) / 2
            e = (r_apo - r_peri) / (r_apo + r_peri)
            t = np.linspace(0, 2 * np.pi, 1000)
            r = a * (1 - e**2) / (1 + e * np.cos(t))
            self.ax.plot(r * np.sin(t), r * np.cos(t), linestyle=linestyle, color=color, label=label)

        # ----- Draw Planet -----
        self.ax.fill(body_radius * np.cos(theta), body_radius * np.sin(theta),
                     color=body_color, zorder=0, label=body_name)

        # ----- Draw circular orbits -----
        draw_orbit(r_min, "dashed", f"Minimum Orbit ({r_min - body_radius} km)", "white")
        draw_orbit(r_max, "dashed", f"Maximum Orbit ({r_max - body_radius} km)", "yellow")

        # ----- Sanity checks -----
        if h_max < h_min or h_ideal < h_min:
            messages.append("❌Signal strength is too low. Increase the number of satellites, antennas, or upgrade the chosen antennas.")
            draw_connection = False

        if r_ideal < body_radius or r_ideal < r_min or r_ideal < r_atm:
            if r_ideal < body_radius:
                messages.append("❌ Ideal orbit below surface! This is impossible!")
            elif r_ideal < r_min:
                messages.append("❌ Ideal orbit is below minimum orbit! This is impossible")
            else:
                messages.append("❌ Ideal orbit within atmosphere! This is highly discouraged!")
            draw_apoapsis = draw_sats = draw_peri_low = draw_apo_high = False

        if r_ideal > soi_altitude:
            messages.append("⚠️ Ideal orbit radius exceeds Sphere Of Influence")

        if r_peri_low < r_atm:
            draw_peri_low = False
            if not is_sync:
                messages.append("⚠️ Lower phasing orbit enters atmosphere! (unsafe)")

        if r_apo_high < r_atm:
            draw_apo_high = False
            if not is_sync:
                messages.append("⚠️ Higher phasing orbit enters atmosphere! (unsafe)")

        if r_apo_high >= soi_altitude:
            messages.append("⚠️ Higher phasing orbit exceeds SOI! (unsafe)")
            draw_apo_high = False

        # ----- Atmosphere -----
        if celestial_body["has_atmosphere"]:
            self.ax.plot(r_atm * np.cos(theta), r_atm * np.sin(theta),
                         linestyle="-", color="grey", linewidth=1)

        # ----- SOI boundary -----
        if is_sync and r_ideal > soi_altitude:
            self.ax.plot(soi_altitude * np.cos(theta), soi_altitude * np.sin(theta),
                         linestyle="dashed", color="red", label="SOI Boundary")

        # ----- Draw orbits and distance labels -----
        if draw_apoapsis:
            self.ax.text(0, r_ideal + 2 * label_offset, "Apoapsis", color="white", ha="center")
            self.ax.scatter(0, r_ideal, marker="o", s=120, color="red", zorder=5)
            self.ax.text(0, -r_ideal + label_offset, f"{h_ideal:.2f} km", color="lime", ha="center", va="bottom")

        label = "Geostationary Orbit" if is_sync else f"Ideal Orbit ({round(r_ideal - body_radius, 2)} km)"
        draw_orbit(r_ideal, "-", label, "lime", 2)

        if draw_peri_low:
            draw_ellipse_from_focus(r_ideal, r_peri_low, "magenta", "dotted",
                                    f"Lower Phasing Orbit ({round(r_peri_low - body_radius, 2)} km)")
            self.ax.text(0, -r_peri_low + 3 * label_offset, f"{r_phase_low - body_radius:.2f} km",
                         color="magenta", ha="center", va="top")

        if draw_apo_high:
            draw_ellipse_from_focus(r_ideal, r_apo_high, "cyan", "dotted",
                                    f"Higher Phasing Orbit ({round(r_apo_high - body_radius, 2)} km)")
            self.ax.text(0, -r_apo_high - 3 * label_offset, f"{r_phase_high - body_radius:.2f} km",
                         color="cyan", ha="center", va="bottom")

        # ----- Satellites -----
        if draw_sats:
            sat_positions = [
                (r_ideal * np.cos(2 * np.pi * i / N), r_ideal * np.sin(2 * np.pi * i / N))
                for i in range(N)
            ]

            for x, y in sat_positions:
                self.ax.scatter(x, y, marker="^", s=120, color="white", edgecolors="black", zorder=5)

            if draw_connection:
                for i in range(N):
                    x1, y1 = sat_positions[i]
                    x2, y2 = sat_positions[(i + 1) % N]
                    self.ax.plot([x1, x2], [y1, y2], color="purple", linewidth=2, zorder=3)

        # ----- Styling -----
        self.ax.plot([0, 0], [0, r_max], color="gray", linestyle="--", linewidth=0.5)
        self.ax.set_aspect("equal")
        self.ax.set_facecolor("black")
        self.fig.patch.set_facecolor("black")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_frame_on(False)
        self.ax.legend(facecolor="black", edgecolor="white", labelcolor="white",
                       loc="center left", bbox_to_anchor=(1, 0.5), fontsize=12)
        self.ax.set_title(
            f"Relay Network around {body_name} ({N} Satellites with {n_antennas} Antennas | Period: {T_str})",
            color="white", fontsize=14
        )
        plt.grid(color="gray", linestyle="--", linewidth=0.3)

        return messages

    # ----- UI helpers -----
    def _set_messages(self, messages):
        self.message_box.configure(state="normal")
        self.message_box.delete("1.0", "end")
        for msg in messages:
            self.message_box.insert("end", msg + "\n")
        self.message_box.configure(state="disabled")

    def _snap_slider(self, var, min_val):
        val = int(var.get())
        if val < min_val:
            val = min_val
        var.set(val)

    def _on_closing(self):
        self.root.quit()

    # ----- Static math helpers -----
    @staticmethod
    def combined_power(P_single: float, n: int, exponent: float = 0.75) -> float:
        """Calculate the combined power of n antennas with a given exponent."""
        return P_single * n ** exponent

    @staticmethod
    def communication_range(P1: float, P2: float) -> float:
        """Calculate the maximum communication range between two antennas."""
        return np.sqrt(P1 * P2)

    @staticmethod
    def solve_for_x(signal: float) -> float:
        """Solve: signal = -2x^3 + 3x^2 using numpy polynomial root finding."""
        # Coefficients for -2x^3 + 3x^2 - signal = 0 (highest degree first)
        roots = np.roots([-2, 3, 0, -signal])
        real_roots = roots[np.isreal(roots)].real
        valid = real_roots[(real_roots >= 0) & (real_roots <= 1)]
        return float(valid[0])

    @staticmethod
    def max_distance(range_val: float, target_signal: float) -> float:
        """Maximum allowed distance for a given signal strength."""
        x = np.floor(RelayNetworkPlanner.solve_for_x(target_signal) * 100) / 100
        return (1 - x) * range_val

    @staticmethod
    def orbital_period(a: float, mu: float) -> float:
        """Orbital period in seconds from semi-major axis in km."""
        return 2 * np.pi * np.sqrt((a * 1000) ** 3 / mu)

    @staticmethod
    def find_altitude_for_period(target_T: float, R_body: float, mu: float) -> float:
        """Solve for altitude (km) that gives a desired orbital period (seconds)."""
        a = ((target_T / (2 * np.pi)) ** 2 * mu) ** (1 / 3)
        return a / 1000 - R_body

    @staticmethod
    def minimum_altitude(R_body: float, N: int) -> float:
        """Minimum geometric altitude (km) for N satellites to maintain line-of-sight."""
        if N < 3:
            raise ValueError("At least 3 satellites required")
        return R_body * (1 / np.cos(np.pi / N) - 1)

    @staticmethod
    def format_kerbal_time(seconds: float) -> str:
        """Convert seconds to Kerbal time string (6-hour days)."""
        seconds = int(seconds)
        kerbal_day = 6 * 3600

        days, seconds = divmod(seconds, kerbal_day)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        return f"{days}d {hours}h {minutes}m {seconds}s"


if __name__ == "__main__":
    app = RelayNetworkPlanner()
    app.root.mainloop()
