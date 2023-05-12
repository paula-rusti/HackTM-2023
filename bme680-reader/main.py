import logging

from config import Configurator


def main():
    main_logger = logging.getLogger("main")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    main_logger.info("Hello world.")

    configurator = Configurator()

    print("")


if __name__ == "__main__":
    main()
