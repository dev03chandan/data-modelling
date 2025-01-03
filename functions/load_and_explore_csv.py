import pandas as pd
def load_and_explore_csv(file_path, text_column, label_column, num_rows_preview=5):
    try:
        # Load the dataset
        data = pd.read_csv(file_path)

        # Validate required columns
        if text_column not in data.columns or label_column not in data.columns:
            return {"error": f"Columns '{text_column}' and '{label_column}' must exist in the dataset."}

        # General information
        num_rows = len(data)
        num_columns = len(data.columns)
        column_names = data.columns.tolist()

        # Null values
        null_values = data.isnull().sum().to_dict()
        null_percent = {col: f"{(val / num_rows) * 100:.2f}%" for col, val in null_values.items()}

        # Label distribution
        label_counts = data[label_column].value_counts().to_dict()
        total_labels = sum(label_counts.values())
        label_distribution = {k: f"{(v / total_labels) * 100:.2f}%" for k, v in label_counts.items()}

        # Text statistics
        text_lengths = data[text_column].dropna().apply(lambda x: len(str(x).split()))
        text_stats = {
            "average_length": text_lengths.mean(),
            "min_length": text_lengths.min(),
            "max_length": text_lengths.max(),
        }

        # Preview the dataset
        preview = data[[text_column, label_column]].head(num_rows_preview).to_dict(orient="records")

        return {
            "status": "success",
            "preview": preview,
            "general_info": {
                "num_rows": num_rows,
                "num_columns": num_columns,
                "column_names": column_names,
            },
            "null_values": {
                "counts": null_values,
                "percentages": null_percent,
            },
            "label_distribution": {
                "counts": label_counts,
                "percentages": label_distribution,
            },
            "text_statistics": text_stats,
        }
    except Exception as e:
        return {"error": str(e)}