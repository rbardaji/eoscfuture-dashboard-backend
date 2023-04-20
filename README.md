# EOSC FUTURE DASHBOARD BACKEND

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>

This repository contains the source code for the RESTful API powering https://env-dashboard.eoscfuture.eu/. It provides access to environmental metrics such as air quality, water quality, and waste management, with robust security measures. The documentation makes integration easy, making it a valuable tool for environmentalists and developers.

## Prerequisites -> MongoDB and FastAPI Installation using Docker Compose

1. Make sure you have Docker and Docker Compose installed on your system. If not, you can download Docker from the [official website](https://www.docker.com/get-started) and follow the instructions for your operating system to install it. If you install the Docker Desktop, Docker Compose may be installed automatically. You can also install Docker Compose by following the instructions on this [link](https://docs.docker.com/compose/install/).

2. We are going to use the existing ```docker-compose.yml``` file in the root of the repo, you can find the file here: [docker-compose.yml](docker-compose.yaml).

3. Run KeyCloak and MongoDB containers by running the following command in the root directory of the repository where the ```docker-compose.yml``` file is located:

```shell
docker-compose up -d
```

## Viewing the Execution Results

Once you have completed the installation steps outlined above and run the command `docker-compose up -d`, the API, MongoDB, and Keycloak will be running on your localhost at the ports specified in the `.env` file. To access these services, you can simply open a web browser and enter the URL of the localhost along with the appropriate port number.

For example, if the API is running on port `8000`, you can access it by entering the URL `http://localhost:8000` in your web browser. Similarly, if MongoDB is running on port `27017`, you can access it by entering `http://localhost:27017`.

You can also view the logs of the running services by running `docker-compose logs -f` command in the root directory of the repository where the `docker-compose.yml` file is located. This will display the logs of all the services in real time.

Additionally, you can check the status of the services by running `docker-compose ps`. This command will show you the current status of all the services running in the compose file.

In order to stop the services, `run docker-compose down` command in the root directory of the repository where the `docker-compose.yaml` file is located.

Please note that the ports and URLs used in the examples above are based on the default settings in the `docker-compose.yaml` file and `.env` file. If you have configured different ports or URLs, you will need to use those instead.

To create a development environment and be able to test or modify the code, you must follow the instructions in [Creating a Development Environment](docs/environment-for-development.md). Once the environment is created, you will be able to run the code and make changes as needed. It is important to remember that any changes you make must be properly tested before they are deployed to production.
