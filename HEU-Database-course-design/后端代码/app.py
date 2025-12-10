from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text

from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
CORS(app)

db = SQLAlchemy(app)


@app.route("/api/health", methods=["GET"])
def health_check():
    """轻量化健康检查，便于前端确认后端存活。"""
    return jsonify({"status": "ok"})


@app.route("/api/buildings/search", methods=["GET"])
def search_buildings():
    """根据楼宇名称模糊查询楼宇信息。"""
    keyword = request.args.get("name", "").strip()
    if not keyword:
        return jsonify({"code": 400, "msg": "请输入要查询的楼宇名称"}), 400

    query_sql = text(
        """
        SELECT building_name,
               area_sqm,
               asking_rent_mb_per_spm_month,
               effective_rent_mb_per_spm_month,
               vacancy_rate
        FROM office_buildings
        WHERE building_name LIKE :keyword
        ORDER BY building_name
        """
    )

    rows = db.session.execute(query_sql, {"keyword": f"%{keyword}%"}).fetchall()
    buildings = [
        {
            "building_name": row[0],
            "area_sqm": row[1],
            "asking_rent_mb_per_spm_month": float(row[2]) if row[2] is not None else None,
            "effective_rent_mb_per_spm_month": float(row[3]) if row[3] is not None else None,
            "vacancy_rate": float(row[4]) if row[4] is not None else None,
        }
        for row in rows
    ]

    return jsonify({"code": 200, "data": buildings, "count": len(buildings)})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
