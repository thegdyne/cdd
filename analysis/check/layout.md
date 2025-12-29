# Layout Analysis: pyro-log-2025-12-28.pdf

## ⚠️  Layout Issues Detected

- 🔴 Page 2: Texts merge: "one" + "sheet."
  - `T2_14` and `T2_15`

## Form Fields (Label -> Input associations)

- Page 1: "NAME:" -> `R1_0` (input_field)
- Page 1: "DATE (end Sunday of week worked):" -> `R1_1` (input_field)
- Page 1: "TRAINEE" -> `R1_2` (checkbox)
- Page 1: "TECHNICIAN" -> `R1_3` (checkbox)
- Page 1: "X" -> `R1_4` (checkbox)
- Page 1: "NAME OF PRODUCTION COMPANY:" -> `R1_5` (input_field)
- Page 1: "FILM/PROGRAMME TITLE:" -> `R1_6` (input_field)
- Page 1: "COUNTRY WORKING IN:" -> `R1_7` (input_field)
- Page 1: "NAME OF PYROTECHNIC SUPERVISOR:" -> `R1_8` (input_field)
- Page 1: "MON" -> `R1_10` (input_field)
- Page 1: "MON" -> `R1_11` (input_field)
- Page 1: "MON" -> `R1_13` (input_field)
- Page 1: "TUES" -> `R1_15` (input_field)
- Page 1: "WED" -> `R1_17` (input_field)
- Page 1: "FRI" -> `R1_19` (input_field)
- Page 1: "FRI" -> `R1_21` (input_field)
- Page 1: "SAT" -> `R1_23` (input_field)
- Page 1: "MON" -> `R1_12` (checkbox)
- Page 1: "TUES" -> `R1_14` (checkbox)
- Page 1: "X" -> `R1_16` (checkbox)
- Page 1: "X" -> `R1_18` (checkbox)
- Page 1: "X" -> `R1_20` (checkbox)
- Page 1: "SAT" -> `R1_22` (checkbox)
- Page 1: "SUN" -> `R1_24` (checkbox)
- Page 1: "Describe Effect required:" -> `R1_25` (text_area)
- Page 1: "Please state type, make and amount of explosives and pyrotechnics used:" -> `R1_26` (text_area)
- Page 2: "of work carried out:" -> `R2_0` (text_area)
- Page 2: "DATE:" -> `R2_1` (input_field)
- Page 2: "SIGNED:" -> `R2_2` (input_field)
- Page 2: "COMMENTS:" -> `R2_3` (text_area)
- Page 2: "(print name):" -> `R2_4` (input_field)
- Page 2: "Signed:" -> `R2_5` (input_field)
- Page 2: "(print name):" -> `R2_6` (input_field)
- Page 2: "Signed:" -> `R2_7` (input_field)

## Detected Tables

- Page 1 at y=160: 3 columns
  Cells: R1_2, R1_3, R1_4

## Usage in Contracts

Reference form fields with source_ref:
```yaml
requirements:
  - id: R001
    source_ref: SRC001#R1_0  # NAME input field
```