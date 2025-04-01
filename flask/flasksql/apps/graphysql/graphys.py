from flask import Blueprint, request, Response
from ariadne import QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL

# 创建蓝图
graphsql_bp = Blueprint('graphysql', __name__, url_prefix='/graphysql')
