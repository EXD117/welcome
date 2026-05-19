import json
import os
from typing import Any, Dict, List, Optional, Callable, Tuple
from abc import ABC, abstractmethod

class Tool(ABC):
    """工具基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """执行工具"""
        pass

class CalculatorTool(Tool):
    """计算器工具"""
    
    def __init__(self):
        super().__init__("calculator", "用于进行数学计算，支持加减乘除运算")
    
    def execute(self, expression: str) -> str:
        try:
            result = eval(expression)
            return f"计算结果: {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"

class WeatherTool(Tool):
    """天气查询工具"""
    
    def __init__(self):
        super().__init__("weather", "用于查询指定城市的天气情况")
    
    def execute(self, city: str) -> str:
        mock_weather = {
            "北京": "晴天，温度25°C",
            "上海": "多云，温度28°C",
            "广州": "阴天，温度32°C",
            "深圳": "小雨，温度30°C"
        }
        return mock_weather.get(city, f"未找到 {city} 的天气信息")

class FileTool(Tool):
    """文件操作工具"""
    
    def __init__(self):
        super().__init__("file", "用于读写文件内容")
    
    def execute(self, action: str, file_path: str, content: str = "") -> str:
        try:
            if action == "read":
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif action == "write":
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"文件 {file_path} 写入成功"
            else:
                return "不支持的操作: " + action
        except Exception as e:
            return f"文件操作错误: {str(e)}"

class AgentConfig:
    """智能体配置"""
    
    def __init__(self, name: str = "智能助手", max_history: int = 10):
        self.name = name
        self.max_history = max_history

class Agent:
    """智能体核心类"""
    
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.tools: List[Tool] = []
        self.history: List[Dict[str, str]] = []
        self._register_default_tools()
    
    def _register_default_tools(self):
        """注册默认工具"""
        self.tools.append(CalculatorTool())
        self.tools.append(WeatherTool())
        self.tools.append(FileTool())
    
    def register_tool(self, tool: Tool):
        """注册自定义工具"""
        self.tools.append(tool)
    
    def get_tool_list(self) -> List[Dict[str, str]]:
        """获取工具列表信息"""
        return [{
            "name": tool.name,
            "description": tool.description
        } for tool in self.tools]
    
    def _add_to_history(self, role: str, content: str):
        """添加对话历史"""
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.config.max_history:
            self.history.pop(0)
    
    def _generate_response(self, prompt: str) -> str:
        """生成响应（模拟LLM）"""
        tool_info = "\n".join([f"- {t.name}: {t.description}" for t in self.tools])
        
        if "计算" in prompt or "加" in prompt or "减" in prompt or "乘" in prompt or "除" in prompt:
            return f"我需要使用计算器工具来帮你计算。\n可用工具: {tool_info}"
        
        if "天气" in prompt:
            return f"我需要使用天气工具来查询天气。\n可用工具: {tool_info}"
        
        if "文件" in prompt or "保存" in prompt or "读取" in prompt:
            return f"我需要使用文件工具来操作文件。\n可用工具: {tool_info}"
        
        return f"你说: {prompt}\n\n我是 {self.config.name}，很高兴为你服务！\n\n可用工具: {tool_info}"
    
    def _parse_tool_call(self, response: str) -> Optional[Tuple[str, Dict[str, Any]]]:
        """解析工具调用"""
        if "calculator" in response.lower():
            return ("calculator", {"expression": "2 + 3 * 4"})
        if "weather" in response.lower():
            return ("weather", {"city": "北京"})
        if "file" in response.lower():
            return ("file", {"action": "read", "file_path": "example.txt"})
        return None
    
    def _execute_tool(self, tool_name: str, params: Dict[str, Any]) -> str:
        """执行工具"""
        for tool in self.tools:
            if tool.name == tool_name:
                try:
                    return tool.execute(**params)
                except Exception as e:
                    return f"工具执行错误: {str(e)}"
        return f"未找到工具: {tool_name}"
    
    def chat(self, user_input: str) -> str:
        """与智能体对话"""
        self._add_to_history("user", user_input)
        
        response = self._generate_response(user_input)
        self._add_to_history("assistant", response)
        
        tool_call = self._parse_tool_call(response)
        if tool_call:
            tool_name, params = tool_call
            tool_result = self._execute_tool(tool_name, params)
            self._add_to_history("tool", f"{tool_name}: {tool_result}")
            response += f"\n\n工具执行结果: {tool_result}"
        
        return response
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.history
    
    def clear_history(self):
        """清空对话历史"""
        self.history = []

def main():
    """示例用法"""
    agent = Agent(AgentConfig(name="我的智能助手"))
    
    print(f"欢迎使用 {agent.config.name}！")
    print("输入 'exit' 或 'quit' 退出对话\n")
    
    while True:
        user_input = input("你: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("再见！")
            break
        
        response = agent.chat(user_input)
        print(f"{agent.config.name}: {response}\n")

if __name__ == "__main__":
    main()