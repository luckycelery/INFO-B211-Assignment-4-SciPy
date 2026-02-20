import pandas as pd
import os
from scipy import stats, interpolate, integrate 

# -----------------------------
# Load Data
# -----------------------------

def load_data(script_dir):
    # Build the full path to your CSV file
    file_path = os.path.join(script_dir, "players_stats_by_season_full_details.csv")

    # Read the CSV into a pandas DataFrame
    return pd.read_csv(file_path)

# -----------------------------
# Filter Data 
# -----------------------------

def filter_nba_regular(data, script_dir):
    # Filter rows where League == "NBA" AND Stage == "Regular_Season"
    reg = data[(data["League"] == "NBA") & (data["Stage"] == "Regular_Season")]

    # Save the filtered dataset to a new CSV file
    reg_output_path = os.path.join(script_dir, "nba_regular_stat.csv")
    reg.to_csv(reg_output_path, index=False)

    return reg

# -----------------------------
# Compute Top Regular Player Stats
# -----------------------------

def most_reg(reg_data, script_dir):
    # Group by player and count how many unique seasons each one played
    seasons_per_player = reg_data.groupby("Player")["Season"].nunique()

    # Identify the player with the highest number of seasons (returns the player's name)
    top_player = seasons_per_player.idxmax()

    # Get the number of seasons that player played
    top_season_count = seasons_per_player.max()

    # Create a DataFrame containing ONLY that player's seasons
    player_df = reg_data[reg_data["Player"] == top_player].sort_values("Season")

    # Save that DataFrame to a CSV so it's easy to reference
    player_output_path = os.path.join(script_dir, "most_reg_player.csv")
    player_df.to_csv(player_output_path, index=False)

    # Return the player's name, number of seasons, and their DataFrame
    return top_player, top_season_count, player_df

def three_point_acc(player_df, script_dir):
    # Make sure that 3PM/3PA values in the player with most reg df are all numeric to count
    df = player_df.copy()
    df["3PM"] = pd.to_numeric(df["3PM"])
    df["3PA"] = pd.to_numeric(df["3PA"])

    # Compute accuracy for each seasonn (each row = new season)
    df["3PAcc"] = df["3PM"]/df["3PA"]

    # Save the 3-point accuracy table for the top player
    threep_output_path = os.path.join(script_dir, "most_reg_player_3p_accuracy.csv")
    df[["Season", "3PM", "3PA", "3PAcc"]].to_csv(threep_output_path, index=False)

    return df[["Season", "3PM", "3PA", "3PAcc"]]

# -----------------------------
# Linear Regression
# -----------------------------

def lin_reg(threep_stats, script_dir):
    # Convert season to numerics
    # Take each season as just the first listed year
    regression_df = threep_stats.copy()
    regression_df["SeasonNum"] = regression_df["Season"].str[:4].astype(int)

    x = regression_df["SeasonNum"]
    y = regression_df["3PAcc"]

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # Create Dataframe to contain Linear Regression stats
    results_df = pd.DataFrame({
        "Metric": ["Slope", "Intercept", "R_squared", "p_value", "Std_Error"],
        "Value": [slope, intercept, r_value**2, p_value, std_err]
    })
    
    # Save dataframe to new CSV file 
    results_path = os.path.join(script_dir, "linear_regression_results.csv") 
    results_df.to_csv(results_path, index=False)

    # Calculate line of best fit based off of linear regression
    regression_df["Best_Fit"] = slope * x + intercept

    # Save the best fit output to new CSV file
    bestfit_path = os.path.join(script_dir, "threep_best_fit_line.csv")
    regression_df[["Season", "3PAcc", "Best_Fit"]].to_csv(bestfit_path, index=False)

    return results_df, regression_df, slope, intercept, r_value, p_value, std_err

# -----------------------------
# 3PA Integration
# -----------------------------

def integrate_best_fit(regression_df, slope, intercept, threep_stats, script_dir):
    # Extract earliest and latest season numbers
    x_start = regression_df["SeasonNum"].min()
    x_end = regression_df["SeasonNum"].max()

    # Define the linear regression function
    def best_fit_func(x):
        return slope * x + intercept

    # Integrate the best-fit line over the played seasons
    area_under_curve, _ = integrate.quad(best_fit_func, x_start, x_end)

    # Compute average predicted accuracy
    avg_predicted_accuracy = area_under_curve / (x_end - x_start)

    # Compute actual average 3P accuracy
    actual_avg_accuracy = threep_stats["3PAcc"].mean()

    # Create DataFrame to store results
    integration_df = pd.DataFrame({
        "Metric": ["Avg_Predicted_Accuracy", "Actual_Avg_Accuracy", "Difference"],
        "Value": [avg_predicted_accuracy, actual_avg_accuracy, avg_predicted_accuracy - actual_avg_accuracy]
    })

    # Save integration results to CSV
    integration_path = os.path.join(script_dir, "integration_comparison_results.csv")
    integration_df.to_csv(integration_path, index=False)

    return integration_df

# -----------------------------
# 3PA Interpolation
# -----------------------------

def interpolate_missing_seasons(regression_df, script_dir):
    # Identify the missing seasons by numeric year
    missing_years = [2002, 2015]  # 2002-2003 and 2015-2016

    # Extract known seasons and accuracy values
    known_x = regression_df["SeasonNum"]
    known_y = regression_df["3PAcc"]

    # Create interpolation function (linear)
    interp_func = interpolate.interp1d(known_x, known_y, fill_value="extrapolate")

    # Compute interpolated values for missing seasons
    interpolated_values = {year: float(interp_func(year)) for year in missing_years}

    # Build a DataFrame for saving
    interp_df = pd.DataFrame({
        "SeasonNum": missing_years,
        "Interpolated_3PAcc": [interpolated_values[yr] for yr in missing_years]
    })

    # Save interpolation results to CSV
    interp_path = os.path.join(script_dir, "interpolated_missing_seasons.csv")
    interp_df.to_csv(interp_path, index=False)

    return interp_df

# -----------------------------
# FGM & FGA Stats
# -----------------------------

def fgm_fga_stats(player_df, script_dir):
    # Ensure numeric types
    df = player_df.copy()

    # Convert to numerics
    df["FGM"] = pd.to_numeric(df["FGM"])
    df["FGA"] = pd.to_numeric(df["FGA"])

    # Compute statistics for FGM
    fgm_mean = df["FGM"].mean()
    fgm_var = df["FGM"].var()
    fgm_skew = stats.skew(df["FGM"])
    fgm_kurt = stats.kurtosis(df["FGM"])

    # Compute statistics for FGA
    fga_mean = df["FGA"].mean()
    fga_var = df["FGA"].var()
    fga_skew = stats.skew(df["FGA"])
    fga_kurt = stats.kurtosis(df["FGA"])

    # Create DataFrame to store results
    fg_stats_df = pd.DataFrame({
        "Metric": ["Mean", "Variance", "Skew", "Kurtosis"],
        "FGM": [fgm_mean, fgm_var, fgm_skew, fgm_kurt],
        "FGA": [fga_mean, fga_var, fga_skew, fga_kurt]
    })

    # Save results to CSV
    fg_stats_path = os.path.join(script_dir, "fg_statistics.csv")
    fg_stats_df.to_csv(fg_stats_path, index=False)

    return fg_stats_df

# -----------------------------
# TTest 
# -----------------------------

def t_tests_fgm_fga(player_df, script_dir):
    # Ensure numeric types
    df = player_df.copy()
    df["FGM"] = pd.to_numeric(df["FGM"])
    df["FGA"] = pd.to_numeric(df["FGA"])

    # Extract the two columns
    fgm = df["FGM"]
    fga = df["FGA"]

    # Perform relational (paired) t-test
    paired_t_stat, paired_p_val = stats.ttest_rel(fgm, fga)

    # Perform regular (independent) t-test
    ind_t_stat, ind_p_val = stats.ttest_ind(fgm, fga)

    # Create DataFrame to store results
    ttest_df = pd.DataFrame({
        "Test_Type": ["Paired t-test", "Independent t-test"],
        "t_statistic": [paired_t_stat, ind_t_stat],
        "p_value": [paired_p_val, ind_p_val]
    })

    # Save results to CSV
    ttest_path = os.path.join(script_dir, "fgm_fga_ttests.csv")
    ttest_df.to_csv(ttest_path, index=False)

    return ttest_df




# -----------------------------
# Main Script
# -----------------------------

# Get the directory where the script is located
script_dir = os.path.dirname(__file__)

# Load the full dataset
df = load_data(script_dir)

# Filter to NBA regular season only
nba_regular = filter_nba_regular(df, script_dir)

# Find the player with the most regular seasons
top_player, top_season_count, player_df = most_reg(nba_regular, script_dir)

# Print results to the console
print("\nPlayer with most regular seasons:", top_player)
print("Number of seasons:", top_season_count)

#Calculate 3-point accuracy for the top player
threep_stats = three_point_acc(player_df, script_dir)

#Print results to console
print("\nThree‑point accuracy by season for:", top_player)
print(threep_stats)

# Perform linear regression for 3PAcc across years played & create line of best fit 
results_df, regression_df, slope, intercept, r_value, p_value, std_err = lin_reg(threep_stats, script_dir)

#Print results to console
print("\nLinear Regression Results")
print("Slope: ", slope)
print("Intercept: ", intercept)
print("R-Value: ", r_value)
print("P-Value: ", p_value)
print("Standard Error: ", std_err)
print("\nLine of Best Fit: \n", regression_df["Best_Fit"])

# Perform integration over played seasons
integration_df = integrate_best_fit(regression_df, slope, intercept, threep_stats, script_dir)

# Print results to console
print("\nIntegration Results:\n", integration_df)

# Interpolate missing seasons (2002-2003 and 2015-2016)
interp_df = interpolate_missing_seasons(regression_df, script_dir)

# Print results to console
print("\nInterpolated Missing Seasons:")
print(interp_df)

# Compute FGM/FGA statistics
fg_stats = fgm_fga_stats(player_df, script_dir)

# Print results to terminal
print("\nFGM vs FGA Statistical Summary:")
print(fg_stats)

# Perform t-tests on FGM and FGA
ttest_df = t_tests_fgm_fga(player_df, script_dir)

# Print results to terminal
print("\nT-Test Results (FGM vs FGA):")
print(ttest_df)

