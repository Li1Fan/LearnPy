from pil_utils import BuildImage, Text2Image


def create_image_with_text(txt, save_path, font_path):
    # 创建文本图片
    name_img = Text2Image.from_text(txt, 60, fontname=font_path, fill="blue", spacing=0, align="center").to_image()
    print(name_img)

    width = max(200, name_img.width)
    height = max(200, name_img.height)

    # 创建一个新的空白图片
    frame = BuildImage.new("RGBA", (width, height), (255, 255, 255, 0))

    # 计算居中位置
    x = (frame.width - name_img.width) // 2  # 计算 x 坐标
    y = (frame.height - name_img.height) // 2  # 计算 y 坐标

    # 将文本图片粘贴到框架中
    frame.paste(name_img, (x, y), alpha=True)

    # 保存图片
    with open(save_path, 'wb') as f:
        f.write(frame.save_jpg().getvalue())

    print(f"图片已保存为 {save_path}")


if __name__ == '__main__':
    font_path = '/home/frz/下载/下载内容/meme-generator-main/resources/fonts/FZSEJW.ttf'
    # create_image_with_text('1×1=1', 'test.jpg', font_path)
    with open('test.txt', 'r') as f:
        for line in f:
            if not line.strip():
                continue
            text, file_name = line.split(" ")
            text = text.split("、")[1]
            file_name = file_name.strip() + '.jpg'
            print(text, file_name)
            create_image_with_text(text, file_name, font_path)
