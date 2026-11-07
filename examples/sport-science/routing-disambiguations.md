# Routing disambiguations (sport-science example)

Two confirmed rulings from a sport-science wiki. Use them as a model for your own `ROUTING.md`.
General principle: route by the **function measured**, not by surface name similarity.

- **RPE for load prescription or progression goes to the CONCEPT `Rate_of_Perceived_Exertion`, NOT the method `Session_RPE`.** `Session_RPE` is specifically Foster's internal-load method (RPE x duration gives AU, monotony, strain). When a paper uses RPE (for example Borg CR-10) to *prescribe and progress* training load rather than to quantify internal load in AU, propagate to the concept (and to `Progressive_Overload` if relevant).
- **`Optojump` (jumping) is not `OptoGait` (running and gait).** Both are Microgate products, but Optojump measures jump height and flight time (a CMJ goes to the method `Countermovement_Jump_Testing`), while OptoGait measures spatiotemporal gait and running parameters. A paper measuring CMJ with Optojump must NOT be added to `OptoGait`.
