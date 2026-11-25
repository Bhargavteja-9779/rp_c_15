# Supplementary Note S6. A decision-support prototype

To show that the workflow fits into routine practice, it is implemented as a small command-line tool that is part of the released code (`src/tool/harvest_tool.py`). Before the season, the owner of the calibration exports a file with the replay quantiles, the variance components and the planner output for each number of reference fruit. In the orchard or packhouse, the user supplies the NIR predictions of the lot's scans (repeated scans of a fruit are allowed and are used for the scale), the reference DMC of the destructively tested fruit and the specification. The tool returns a corrected prediction and a lower bound for every fruit, a HARVEST or WAIT/RE-TEST flag per fruit, a lot recommendation, a plain-language statement of what the bound guarantees, and the planned interval width for other numbers of reference fruit.

Box 1 shows the output for one lot of the 2021 season, calibrated on 2015–2020 and chosen as the lot of median size before its result was seen, with ten reference fruit and a specification of 15 % DMC.

> **Box 1.** Output of the prototype for lot {{r.demo['demo_lot']}} (2021), *m* = 10, specification 15 % DMC.
>
> Lot bias correction: {{f"{r.demo['lot_bias_correction']:+.2f}"}} % DMC · lot scale: {{f"{r.demo['lot_scale']:.2f}"}} · fruit cleared for harvest: {{r.demo['fruit_cleared_for_harvest']}} · **lot recommendation: {{r.demo['lot_recommendation']}}**
>
> Statement: {{r.demo['statement']}}
>
> Planned two-sided width (% DMC) for m = 0, 3, 5, 10, 20, 30: {{", ".join(f"{v:.2f}" for v in r.demo['planner_two_sided_width_by_m'].values())}}
>
> Check against the reference values of the {{r.demo['demo_truth']['fruit_evaluated']}} non-reference fruit (not available to the tool): truly compliant {{r.demo['demo_truth']['truly_compliant']}}; lower bounds that held {{r.demo['demo_truth']['lower_bound_coverage']}}.

In this lot the calibration over-predicted DMC by about {{f"{-r.demo['lot_bias_correction']:.1f}"}} % points. The ten reference fruit exposed the bias and the tool recommended waiting. The reference values, unknown to the tool, confirm that none of the fruit had reached the specification. A single lot proves nothing about performance, which is the subject of Supplementary Note S7; the box shows the form in which the result would reach a user. The prototype is a research tool. Its use in practice would need an interface on the instrument or a phone, a calibration file maintained by the instrument provider or packhouse, and the prospective validation discussed in Section 6.
