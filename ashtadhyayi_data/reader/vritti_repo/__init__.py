import frontmatter
import logging

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)


def get_vRtti_sequence_map(vritti_id):
    pass


if __name__ == '__main__':
    get_vRtti_sequence_map(vritti_id='balamanorama')