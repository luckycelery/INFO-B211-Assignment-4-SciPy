# INFO-B211 — Assignment 4 (SciPy)

---

## **Answers to Additional Questions**

---

### **1. How does the integrated predicted 3‑point accuracy compare to the actual average?**

| Metric                         | Value     |
|--------------------------------|-----------|
| Avg predicted accuracy         | 0.370083  |
| Actual average accuracy        | 0.369950  |
| Difference                     | 0.000132  |

The regression‑based predicted average is **0.000132 higher** than the actual average.  
This difference is extremely small (≈0.013 percentage points), meaning the regression line fits Vince Carter’s long‑term 3‑point accuracy **very closely**.

---

### **2. How do the FGM statistics compare to the FGA statistics?**

| Metric     | FGM        | FGA         |
|------------|------------|-------------|
| Mean       | 445.26     | 1024.74     |
| Variance   | 55,558     | 249,961     |
| Skew       | –0.083     | –0.146      |
| Kurtosis   | –1.432     | –1.488      |

**Mean**  
FGA is much higher than FGM — expected because attempts > makes. The ratio aligns with his career FG% (~43–45%).

**Variance**  
FGA variance is **4.5× larger**, meaning his shot attempts fluctuated more season‑to‑season than his makes.

**Skew**  
Both slightly negative, indicating a few lower‑volume seasons and most seasons clustered toward the higher end.

**Kurtosis**  
Both strongly negative (platykurtic), meaning his shooting volume was **consistent** with few extreme outliers.

**Overall comparison**  
FGA is larger and more variable, but the *shape* of both distributions is similar. This shows that attempts and makes scaled together consistently across his career.

---

### **3. How does the paired t‑test compare to the independent t‑test?**

| Test Type            | t‑statistic | p‑value      |
|----------------------|-------------|--------------|
| Paired t‑test        | –9.514      | 1.91e‑08     |
| Independent t‑test   | –4.570      | 5.55e‑05     |

**Paired t‑test**  
Uses season‑by‑season pairing (FGM and FGA from the same season).  
Produces a **much larger magnitude t‑statistic** and **much smaller p‑value**, meaning it detects the difference more strongly.

**Independent t‑test**  
Treats FGM and FGA as unrelated samples.  
Produces a weaker t‑statistic and larger p‑value because it ignores the natural pairing in the data.

**Conclusion**  
Both tests show FGA is significantly higher than FGM, but the **paired t‑test is far more appropriate and sensitive** for this dataset because it accounts for season‑to‑season pairing.

---

## **Project Purpose** 
The purpose of this project is to demonstrate the use of SciPy and pandas for: 
  - data filtering and preprocessing
  - computing per‑season shooting accuracy
  - performing linear regression
  - integrating a regression line to estimate long‑term averages
  - interpolating missing values
  - computing descriptive statistics
  - performing paired and independent t‑tests
The analysis is applied to the NBA player with the most regular seasons played (Vince Carter), allowing us to examine long‑term trends in shooting accuracy and field‑goal performance.

---

## Program Structure and Function Design

The project is implemented using a modular, function‑based design. Each function performs one clear task, produces well‑defined outputs, and saves its results to a CSV file for transparency and reproducibility.

### 1. `load_data(script_dir)`
**Purpose:** Loads the full dataset from CSV.  
**Inputs:** Directory path.  
**Outputs:** Full pandas DataFrame.

---

### 2. `filter_nba_regular(data, script_dir)`
**Purpose:** Filters the dataset to NBA regular‑season rows only.  
**Inputs:** Full dataset, directory path.  
**Outputs:** Filtered DataFrame and `nba_regular_stat.csv`.

---

### 3. `most_reg(reg_data, script_dir)`
**Purpose:** Identifies the player with the most regular seasons played.  
**Inputs:** Filtered NBA regular‑season data.  
**Outputs:** Player name, number of seasons, player‑specific DataFrame, and `most_reg_player.csv`.

---

### 4. `three_point_acc(player_df, script_dir)`
**Purpose:** Computes 3‑point accuracy (3PM ÷ 3PA) for each season.  
**Inputs:** Player DataFrame.  
**Outputs:** Accuracy DataFrame and `most_reg_player_3p_accuracy.csv`.

---

### 5. `lin_reg(threep_stats, script_dir)`
**Purpose:** Performs linear regression on 3‑point accuracy over time.  
**Inputs:** 3‑point accuracy DataFrame.  
**Outputs:** Regression statistics, regression‑enhanced DataFrame, and two CSV outputs:  
- `linear_regression_results.csv`  
- `threep_best_fit_line.csv`

---

### 6. `integrate_best_fit(regression_df, slope, intercept, threep_stats, script_dir)`
**Purpose:** Integrates the regression line to compute the predicted average 3‑point accuracy.  
**Inputs:** Regression DataFrame, regression parameters, raw accuracy data.  
**Outputs:** Comparison DataFrame and `integration_comparison_results.csv`.

---

### 7. `interpolate_missing_seasons(regression_df, script_dir)`
**Purpose:** Estimates missing 3‑point accuracy values for seasons the player did not play (2002–2003 and 2015–2016).  
**Inputs:** Regression DataFrame.  
**Outputs:** Interpolation DataFrame and `interpolated_missing_seasons.csv`.

---

### 8. `fgm_fga_stats(player_df, script_dir)`
**Purpose:** Computes mean, variance, skew, and kurtosis for FGM and FGA.  
**Inputs:** Player DataFrame.  
**Outputs:** Statistics DataFrame and `fg_statistics.csv`.

---

### 9. `t_tests_fgm_fga(player_df, script_dir)`
**Purpose:** Performs both a paired t‑test and an independent t‑test on FGM vs FGA.  
**Inputs:** Player DataFrame.  
**Outputs:** T‑test results DataFrame and `fgm_fga_ttests.csv`.

---

## Limitations

This project uses the full dataset but **reduces it to NBA regular‑season data only**.  
This filtering step excludes:

- preseason games  
- playoff games  
- international leagues  
- partial seasons outside the NBA  

All subsequent analysis is based solely on the player’s NBA regular‑season performance.  
No other limitations were added to the implementation.







