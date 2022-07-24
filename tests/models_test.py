from app import Image, db
import unittest


class SimpleTest(unittest.TestCase):
    def test(self):
        imgname, imgurl, imgdetails = "image1", "/images/image1.jpg", "720x720"
        img = Image(ImgName=imgname, ImgURL=imgurl, ImgDetails=imgdetails)
        op = "{\n\tName: %s,\n\turl: %s,\n\tdetails: %s\n}" % (
            imgname,
            imgurl,
            imgdetails,
        )
        assert str(img) == op


if __name__ == "__main__":
    unittest.main()
