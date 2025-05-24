import google.generativeai as genai
from PIL import Image
import os
import imghdr  # 用于检测图片类型
from config import GOOGLE_API_KEY

def analyze_building(image_path, description):
    try:
        # 配置 Gemini API 密钥
        genai.configure(api_key=GOOGLE_API_KEY)

        # 检查图片有效性
        if not os.path.exists(image_path):
            raise ValueError("图片路径不存在")
        
        # 自动检测图片类型
        image_type = imghdr.what(image_path)
        if image_type not in ['jpeg', 'png', 'bmp']:
            raise ValueError(f"不支持的图片格式：{image_type}")
        
        # 打开图片
        img = Image.open(image_path)

        # 验证必填字段（示例）
        required_fields = ['name', 'address', 'type']
        for field in required_fields:
            if not description.get(field):
                raise ValueError(f"必填字段缺失：{field}")

        # 构建提示词
        description_text = "\n".join([
            f"名称：{description.get('name', '无')}",
            f"地址：{description.get('address', '无')}",
            f"高度/层数：{description.get('height', '无')}",
            f"结构类型：{description.get('type', '无')}",
            f"建成年代：{description.get('built_year', '无')}",
            f"使用情况：{description.get('usage', '无')}",
            f"维修记录：{description.get('repair_history', '无')}",
            f"灾害记录：{description.get('disaster_history', '无')}",
        ])

        prompt = f"""
{description_text}这是额外补充信息，如果不是“无”，请参考，如果是“无”，请忽略；然后
        此处省略结构化提示词模板
        """

        # 加载模型
        model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')

        # 发送请求（文本 + 图片）
        response = model.generate_content([prompt, img])

        # 返回分析结果
        return response.text

    except ValueError as e:
        # 处理参数验证错误
        return f"输入错误：{str(e)}"

    except Exception as e:
        # 捕获其他所有异常
        return f"未知错误：{str(e)}"