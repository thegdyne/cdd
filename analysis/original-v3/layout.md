# Layout Analysis: WeeklyPyrotechnicLog_4.pdf

## Form Fields (Label -> Input associations)

- Page 1: "NAME:" -> `R1_117` (input_field)
- Page 1: "NAME OF PRODUCTION COMPANY:" -> `R1_118` (input_field)
- Page 1: "FILM/PROGRAMME TITLE:" -> `R1_122` (input_field)
- Page 1: "COUNTRY WORKING IN:" -> `R1_121` (input_field)
- Page 1: "NAME OF PYROTECHNIC SUPERVISOR:" -> `R1_120` (input_field)
- Page 1: "MON" -> `R1_46` (checkbox)
- Page 1: "TUES" -> `R1_47` (checkbox)
- Page 1: "WED" -> `R1_48` (checkbox)
- Page 1: "THURS" -> `R1_49` (checkbox)
- Page 1: "FRI" -> `R1_50` (checkbox)
- Page 1: "SAT" -> `R1_51` (checkbox)
- Page 1: "SUN" -> `R1_52` (checkbox)
- Page 2: "DATE:" -> `R2_38` (input_field)
- Page 2: "(print name):" -> `R2_39` (input_field)
- Page 2: "(print name):" -> `R2_41` (input_field)
- Page 2: "(print name):" -> `R2_40` (input_field)
- Page 2: "Signed:" -> `R2_42` (input_field)

## Detected Tables

- Page 1 at y=145: 3 columns
  Cells: R1_2, R1_3, R1_4
- Page 1 at y=310: 15 columns
  Cells: R1_53, R1_54, R1_55, R1_56, R1_57, R1_58, R1_59, R1_60, R1_61, R1_62, R1_63, R1_64, R1_65, R1_66, R1_67
- Page 1 at y=315: 15 columns
  Cells: R1_68, R1_46, R1_72, R1_47, R1_75, R1_48, R1_78, R1_49, R1_81, R1_50, R1_84, R1_51, R1_87, R1_52, R1_90
- Page 1 at y=325: 17 columns
  Cells: R1_69, R1_70, R1_71, R1_73, R1_74, R1_76, R1_77, R1_79, R1_80, R1_82, R1_83, R1_85, R1_86, R1_88, R1_89, R1_91, R1_92
- Page 1 at y=435: 5 columns
  Cells: R1_99, R1_100, R1_101, R1_103, R1_104
- Page 1 at y=670: 5 columns
  Cells: R1_111, R1_112, R1_113, R1_115, R1_116
- Page 2 at y=150: 5 columns
  Cells: R2_6, R2_7, R2_8, R2_10, R2_11
- Page 2 at y=340: 5 columns
  Cells: R2_18, R2_19, R2_20, R2_22, R2_23
- Page 2 at y=585: 5 columns
  Cells: R2_25, R2_26, R2_27, R2_28, R2_29
- Page 2 at y=635: 5 columns
  Cells: R2_31, R2_32, R2_33, R2_35, R2_36

## Usage in Contracts

Reference form fields with source_ref:
```yaml
requirements:
  - id: R001
    source_ref: SRC001#R1_0  # NAME input field
```