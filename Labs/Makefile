.PHONY: all fetch analyze clean

# Set analyze as the default target
all: analyze

fetch:
	@echo "Starting to fetch METAR data..."
	./fetch_metars.sh
	@echo "Finished fetching data. Files saved in raw_metars/."

analyze: fetch
	@echo "Starting to analyze METAR data..."
	./analyze_data.sh
	@echo "Finished analyzing data. Report saved to weather_report.csv."
	@echo "Pipeline completed successfully."

clean:
	@echo "Cleaning up generated data..."
	rm -rf raw_metars weather_report.csv
	@echo "Clean complete. All generated files removed."

