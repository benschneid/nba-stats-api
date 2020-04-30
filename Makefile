.PHONY: run build

build:
	sudo docker build --rm -t puckel/docker-airflow .

run: 
	#sudo docker run -d -p 8080:8080 puckel/docker-airflow
	#@echo airflow running on http://localhost:8080
	docker-compose -f docker-compose-LocalExecutor.yml up -d

kill:
	@echo "Killing docker-airflow containers"
	sudo docker stop $(shell sudo docker ps -q)
	sudo docker rm $(shell sudo docker ps -q)

tty:
	sudo docker exec -i -t $(shell sudo docker ps -q --filter ancestor=puckel/docker-airflow)
