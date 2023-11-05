
1. Pull the latest changes:
```bash
git pull
```

2. Working in this directory, build the docker image with the build script, with the -l flag to add a 'latest' tag to the image:
```bash

./build.sh -l
```

3. Always working in this directory, use docker compose to start the container running kernel planckster:
```bash
docker compose up -d
```

4. Get a shell inside the container:
```bash
docker exec -it kernel-planckster bash
```

5. To activate the environment with the python dependencies, inside the container:
```bash
poetry shell
```

Inside the container, you can do git pull if the main repo has

6. Working in this directory, stop and remove the container:
```bash
docker compose down
```