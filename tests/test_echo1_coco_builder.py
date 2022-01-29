from echo1_coco_builder import __version__
from echo1_coco_builder import __version__
from echo1_coco_builder.echo1_coco_builder import CocoBuilder
import pandas as pd, re


def string_to_list_int(a_string, sep=","):
    return a_string.split(sep)


def test_builder():

    # Open a CSV using pandas
    df = pd.read_csv("test.csv")

    # Initialize the coco generator
    coco_builder = CocoBuilder()

    # For each row in the csv
    for annotation_id, row in df.iterrows():

        # image_id must be an integer
        image_id = int(re.sub("[^0-9]", "", row["image_name"]))

        # image_name must be a string
        file_name = row["image_name"]

        # image_width and image_height must be an integer
        image_width = row["image_width"]
        image_height = row["image_height"]

        # category_id must be an integer
        category_id = row["category_id"]

        # category_name must be a string
        category_name = row["category_name"]

        # bbox format: [x,y,width,height]
        img_coords_str_list = row["bbox"].split(",")

        x_min, y_min, x_max, y_max = map(int, img_coords_str_list)

        bbox = [x_min, y_min, x_max - x_min, y_max - y_min]

        area = (x_max - x_min) * (y_max - y_min)

        segmentation = [
            [
                x_min,
                y_min,
                x_min,
                (y_min + y_max),
                (x_min + x_max),
                (y_min + y_max),
                (x_min + x_max),
                y_min,
            ]
        ]

        # add a new image
        coco_builder.add_image(
            {
                "id": image_id,
                "file_name": file_name,
                "width": image_width,
                "height": image_height,
            }
        )

        # add a new category
        coco_builder.add_category({"id": category_id, "name": category_name})

        # add a new annotation
        coco_builder.add_annotation(
            {
                "id": row[0],
                "image_id": image_id,
                "category_id": category_id,
                "bbox": bbox,
                "segmentation": segmentation,
                "iscrowd": 0,
                "area": area,
            }
        )

    # add info
    coco_builder.add_info(
        {
            "year": 2022,
            "version": "v1.0",
            "contributor": "Echo1",
            "description": "Contact for more info.",
            "url": "https://echo1.io",
        }
    )

    # images assertion
    assert len(coco_builder.images) == 2
    for image in coco_builder.images:
        assert type(image["id"]) is int
        assert type(image["width"]) is int
        assert type(image["height"]) is int
        assert type(image["file_name"]) is str

    # annotations assertion
    assert len(coco_builder.annotations) == 5
    for annotation in coco_builder.annotations:
        assert type(annotation["id"]) is int
        assert type(annotation["image_id"]) is int
        assert type(annotation["iscrowd"]) is int
        assert type(annotation["area"]) is float
        assert len(annotation["segmentation"]) == 1

    # categories assertion
    assert len(coco_builder.categories) == 2
    for category in coco_builder.categories:
        assert type(category["id"]) is int
        assert type(category["name"]) is str

    # info assertion
    assert type(coco_builder.info["year"]) is int
    assert coco_builder.info["year"] == 2022
    assert type(coco_builder.info["version"]) is str
    assert coco_builder.info["version"] == "v1.0"
    assert type(coco_builder.info["description"]) is str
    assert coco_builder.info["description"] == "Contact for more info."
    assert type(coco_builder.info["contributor"]) is str
    assert coco_builder.info["contributor"] == "Echo1"
    assert type(coco_builder.info["url"]) is str
    assert coco_builder.info["url"] == "https://echo1.io"
