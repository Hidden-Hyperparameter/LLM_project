setup:
	@echo "Setting up the environment"
	@bash utils/install.sh

build:
	@echo "Building the project"
	@python run_process.py

add: data_list.txt
	@python add_book.py

run:
	@echo "Running the UI"
	@python webUI.py

clean:
	@rm debug.log