"""
IELTS Score Analyzer - AI Document Summarizer
Backend API using Flask + Optional LLM Integration
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Optional: LLM Integration (uncomment and configure as needed)
# from openai import OpenAI
# from anthropic import Anthropic

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# IELTS Band Descriptions
BAND_DESCRIPTIONS = {
    9: "Expert User - Thành thạo hoàn toàn",
    8: "Very Good User - Rất thành thạo", 
    7: "Good User - Thành thạo",
    6: "Competent User - Đủ năng lực",
    5: "Modest User - Khiêm tốn",
    4: "Limited User - Hạn chế",
    3: "Extremely Limited - Rất hạn chế",
    2: "Intermittent User - Không ổn định",
    1: "Non User - Không sử dụng được"
}

# Skill names in Vietnamese
SKILL_NAMES = {
    'listening': 'Nghe (Listening)',
    'speaking': 'Nói (Speaking)',
    'reading': 'Đọc (Reading)',
    'writing': 'Viết (Writing)'
}

# Comprehensive recommendations database
RECOMMENDATIONS = {
    'listening': {
        'low': [
            "Nghe podcast tiếng Anh hàng ngày (BBC Learning English, IELTS Liz, 6 Minute English)",
            "Xem phim/series có phụ đề tiếng Anh, sau đó dần bỏ phụ đề",
            "Luyện nghe với các bài test IELTS Listening thực tế từ Cambridge",
            "Tập nghe các giọng khác nhau: British, American, Australian",
            "Sử dụng app như ELSA Speak hoặc Speechling để cải thiện khả năng nghe"
        ],
        'medium': [
            "Tăng độ khó bằng cách nghe TED Talks, documentaries",
            "Practice note-taking skills khi nghe các bài giảng academic",
            "Làm quen với tất cả các dạng câu hỏi IELTS Listening",
            "Nghe và shadowing theo để cải thiện cả speaking lẫn listening"
        ],
        'high': [
            "Duy trì bằng cách nghe tin tức quốc tế hàng ngày (BBC, CNN)",
            "Thử thách bản thân với academic lectures từ Coursera, edX",
            "Luyện nghe các chủ đề chuyên ngành phức tạp"
        ]
    },
    'speaking': {
        'low': [
            "Thực hành nói mỗi ngày, tự ghi âm và nghe lại để tự đánh giá",
            "Tìm partner luyện Speaking hoặc sử dụng app như Cambly, iTalki",
            "Học và luyện các topic thường gặp trong IELTS Speaking Part 1, 2, 3",
            "Xây dựng vocabulary theo chủ đề với collocations và phrases",
            "Tập phát âm đúng các âm khó và luyện word stress"
        ],
        'medium': [
            "Tập trả lời câu hỏi Part 2 với cue card trong 2 phút",
            "Học cách phát triển ý tưởng và đưa ví dụ cụ thể",
            "Cải thiện pronunciation, intonation và connected speech",
            "Học cách sử dụng fillers tự nhiên và tránh ngập ngừng"
        ],
        'high': [
            "Thực hành tranh luận và thảo luận các chủ đề phức tạp",
            "Học idioms, phrasal verbs và advanced vocabulary",
            "Tập paraphrase câu hỏi và sử dụng ngôn ngữ đa dạng"
        ]
    },
    'reading': {
        'low': [
            "Đọc sách báo tiếng Anh hàng ngày (The Guardian, BBC News, The Economist)",
            "Bắt đầu với các bài đọc ngắn phù hợp level, từ từ tăng độ dài",
            "Học kỹ năng skimming (đọc lướt) và scanning (tìm thông tin cụ thể)",
            "Xây dựng vocabulary thông qua đọc và ghi chép từ mới vào flashcard",
            "Sử dụng app như Kindle với dictionary tích hợp"
        ],
        'medium': [
            "Làm quen với tất cả các dạng bài Reading IELTS (True/False/NG, Matching, etc.)",
            "Tập đọc nhanh và tìm thông tin hiệu quả trong thời gian giới hạn",
            "Đọc academic articles và research papers để quen với văn phong học thuật",
            "Học cách identify main ideas và supporting details"
        ],
        'high': [
            "Đọc các tài liệu chuyên ngành phức tạp (journals, reports)",
            "Cải thiện tốc độ đọc mà vẫn duy trì comprehension cao",
            "Đọc và phân tích các bài văn argumentative"
        ]
    },
    'writing': {
        'low': [
            "Viết nhật ký bằng tiếng Anh mỗi ngày để tạo thói quen",
            "Học cấu trúc bài luận IELTS Task 1 (report) và Task 2 (essay)",
            "Luyện viết câu phức (complex sentences) với linking words",
            "Nhờ giáo viên hoặc native speaker chữa bài viết và học từ feedback",
            "Học các mẫu câu academic writing phổ biến"
        ],
        'medium': [
            "Tập phân tích đề và lập dàn ý (outline) trước khi viết",
            "Học cách paraphrase hiệu quả và sử dụng synonyms đa dạng",
            "Viết ít nhất 2-3 bài essay mỗi tuần và tự chấm theo rubric",
            "Học cách viết introduction và conclusion ấn tượng"
        ],
        'high': [
            "Tập viết các bài luận phức tạp với nhiều góc nhìn khác nhau",
            "Cải thiện academic vocabulary và formal expressions",
            "Học cách sử dụng ví dụ và data để support arguments"
        ]
    }
}


def calculate_overall(scores: dict) -> float:
    """Calculate overall IELTS band score"""
    total = sum(scores.values())
    avg = total / 4
    # Round to nearest 0.5
    return round(avg * 2) / 2


def get_score_level(score: float) -> str:
    """Categorize score level"""
    if score >= 7:
        return 'high'
    elif score >= 5:
        return 'medium'
    return 'low'


def get_band_description(score: float) -> str:
    """Get band description for a score"""
    band = int(score)
    band = max(1, min(9, band))
    return BAND_DESCRIPTIONS.get(band, "")


def analyze_scores_rule_based(scores: dict, student_name: str) -> dict:
    """
    Rule-based analysis of IELTS scores
    Returns structured analysis with summary, strengths, weaknesses, recommendations
    """
    overall = calculate_overall(scores)
    
    # Create skill array with scores
    skills = [
        {'name': 'listening', 'score': scores['listening'], 'label': SKILL_NAMES['listening']},
        {'name': 'speaking', 'score': scores['speaking'], 'label': SKILL_NAMES['speaking']},
        {'name': 'reading', 'score': scores['reading'], 'label': SKILL_NAMES['reading']},
        {'name': 'writing', 'score': scores['writing'], 'label': SKILL_NAMES['writing']}
    ]
    
    # Sort by score
    sorted_skills = sorted(skills, key=lambda x: x['score'], reverse=True)
    strengths = [s for s in sorted_skills if s['score'] >= overall]
    weaknesses = [s for s in sorted_skills if s['score'] < overall]
    
    # Generate summary
    summary_parts = [f"Học viên {student_name} đạt điểm IELTS tổng thể {overall}."]
    
    if strengths:
        strength_names = [s['label'].split(' ')[0] for s in strengths]
        summary_parts.append(f"Có khả năng {' và '.join(strength_names)} tốt")
        if strengths[0]['score'] >= 7:
            summary_parts[-1] += f" với điểm nổi bật ở kỹ năng {strengths[0]['label'].split(' ')[0]} ({strengths[0]['score']})."
        else:
            summary_parts[-1] += "."
    
    if weaknesses:
        weakness_names = [w['label'].split(' ')[0] for w in weaknesses]
        summary_parts.append(
            f"Tuy nhiên, {' và '.join(weakness_names)} còn hạn chế "
            "do có thể chưa thường xuyên luyện tập các kỹ năng này."
        )
    
    summary = " ".join(summary_parts)
    
    # Generate recommendations for weak skills
    recommendations_list = []
    for skill in weaknesses:
        level = get_score_level(skill['score'])
        skill_recs = RECOMMENDATIONS[skill['name']][level]
        recommendations_list.append({
            'skill': skill['label'],
            'score': skill['score'],
            'items': skill_recs
        })
    
    # Also add some recommendations for maintaining strengths
    for skill in strengths[:1]:  # Top strength
        level = get_score_level(skill['score'])
        skill_recs = RECOMMENDATIONS[skill['name']][level]
        recommendations_list.append({
            'skill': skill['label'] + ' (Duy trì)',
            'score': skill['score'],
            'items': skill_recs[:2]  # Just top 2 recommendations
        })
    
    # Generate action items
    action_items = []
    if weaknesses:
        weakest = weaknesses[-1]
        action_items.append(
            f"Ưu tiên cải thiện kỹ năng {weakest['label'].split(' ')[0]} "
            f"(hiện tại: {weakest['score']}, mục tiêu: {min(9, weakest['score'] + 1)})"
        )
    
    action_items.extend([
        f"Đặt mục tiêu đạt {min(9, overall + 0.5)} trong 3 tháng tới",
        "Luyện tập ít nhất 2 tiếng mỗi ngày, tập trung vào các kỹ năng yếu",
        "Làm mock test đầy đủ 2 tuần/lần để theo dõi tiến độ",
        "Tham gia study group hoặc tìm tutor để được hướng dẫn"
    ])
    
    return {
        'student_name': student_name,
        'overall': overall,
        'band_description': get_band_description(overall),
        'skills': skills,
        'strengths': [
            {'skill': s['label'], 'score': s['score'], 
             'status': 'Xuất sắc' if s['score'] >= 7 else 'Tốt'}
            for s in strengths
        ],
        'weaknesses': [
            {'skill': w['label'], 'score': w['score'], 'status': 'Cần cải thiện'}
            for w in weaknesses
        ],
        'summary': summary,
        'recommendations': recommendations_list,
        'action_items': action_items,
        'analyzed_at': datetime.now().isoformat()
    }


def analyze_with_llm(scores: dict, student_name: str, provider: str = 'openai') -> dict:
    """
    Use LLM (GPT-4 / Claude) for more sophisticated analysis
    Falls back to rule-based if API not configured
    """
    # Prepare the prompt
    prompt = f"""Bạn là một chuyên gia tư vấn IELTS. Hãy phân tích điểm IELTS của học viên và đưa ra nhận xét, đề xuất cải thiện.

Thông tin học viên:
- Tên: {student_name}
- Listening: {scores['listening']}
- Speaking: {scores['speaking']}  
- Reading: {scores['reading']}
- Writing: {scores['writing']}

Hãy phân tích và đưa ra:
1. Tóm tắt đánh giá tổng thể (2-3 câu)
2. Điểm mạnh của học viên
3. Điểm yếu cần cải thiện
4. Đề xuất cụ thể cho từng kỹ năng yếu (resources, phương pháp học)
5. Action items - kế hoạch hành động cụ thể trong 1-3 tháng

Trả lời bằng tiếng Việt, ngắn gọn và thực tế."""

    # Try OpenAI
    if provider == 'openai' and OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Bạn là chuyên gia tư vấn IELTS với nhiều năm kinh nghiệm."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            llm_analysis = response.choices[0].message.content
            
            # Combine with rule-based analysis
            base_analysis = analyze_scores_rule_based(scores, student_name)
            base_analysis['llm_analysis'] = llm_analysis
            base_analysis['llm_provider'] = 'OpenAI GPT-4'
            return base_analysis
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
    
    # Try Anthropic Claude
    if provider == 'anthropic' and ANTHROPIC_API_KEY:
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=ANTHROPIC_API_KEY)
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            llm_analysis = response.content[0].text
            
            base_analysis = analyze_scores_rule_based(scores, student_name)
            base_analysis['llm_analysis'] = llm_analysis
            base_analysis['llm_provider'] = 'Anthropic Claude'
            return base_analysis
            
        except Exception as e:
            print(f"Anthropic API error: {e}")
    
    # Fallback to rule-based
    return analyze_scores_rule_based(scores, student_name)


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint to analyze IELTS scores"""
    try:
        data = request.json
        
        # Validate input
        required_fields = ['student_name', 'listening', 'speaking', 'reading', 'writing']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        scores = {
            'listening': float(data['listening']),
            'speaking': float(data['speaking']),
            'reading': float(data['reading']),
            'writing': float(data['writing'])
        }
        
        # Validate score ranges
        for skill, score in scores.items():
            if not 0 <= score <= 9:
                return jsonify({'error': f'Invalid {skill} score. Must be 0-9'}), 400
        
        student_name = data['student_name']
        use_llm = data.get('use_llm', False)
        llm_provider = data.get('llm_provider', 'openai')
        
        # Perform analysis
        if use_llm:
            analysis = analyze_with_llm(scores, student_name, llm_provider)
        else:
            analysis = analyze_scores_rule_based(scores, student_name)
        
        return jsonify(analysis)
        
    except ValueError as e:
        return jsonify({'error': f'Invalid score value: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export', methods=['POST'])
def export_report():
    """Export analysis as text/PDF report"""
    try:
        data = request.json
        analysis = data.get('analysis', {})
        
        # Generate report content
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           IELTS SCORE ANALYSIS REPORT                        ║
║           BÁO CÁO PHÂN TÍCH ĐIỂM IELTS                       ║
╚══════════════════════════════════════════════════════════════╝

📅 Ngày phân tích: {datetime.now().strftime('%d/%m/%Y %H:%M')}
👤 Học viên: {analysis.get('student_name', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 ĐIỂM TỔNG THỂ: {analysis.get('overall', 0)}
   {analysis.get('band_description', '')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 CHI TIẾT ĐIỂM:
"""
        for skill in analysis.get('skills', []):
            bar_length = int(skill['score'] / 9 * 20)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            report += f"   • {skill['label']}: {skill['score']} [{bar}]\n"

        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 TÓM TẮT ĐÁNH GIÁ:
{analysis.get('summary', '')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💪 ĐIỂM MẠNH:
"""
        for s in analysis.get('strengths', []):
            report += f"   ✓ {s['skill']}: {s['score']} - {s['status']}\n"

        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📉 ĐIỂM CẦN CẢI THIỆN:
"""
        for w in analysis.get('weaknesses', []):
            report += f"   ⚠ {w['skill']}: {w['score']} - {w['status']}\n"

        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 ĐỀ XUẤT CẢI THIỆN:
"""
        for rec in analysis.get('recommendations', []):
            report += f"\n   📌 {rec['skill']}:\n"
            for item in rec['items']:
                report += f"      → {item}\n"

        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 KẾ HOẠCH HÀNH ĐỘNG:
"""
        for i, action in enumerate(analysis.get('action_items', []), 1):
            report += f"   {i}. {action}\n"

        if 'llm_analysis' in analysis:
            report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 PHÂN TÍCH AI ({analysis.get('llm_provider', 'AI')}):
{analysis['llm_analysis']}
"""

        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Báo cáo được tạo bởi IELTS Score Analyzer - AI Document Summarizer
"""

        # Return as downloadable file
        buffer = BytesIO()
        buffer.write(report.encode('utf-8'))
        buffer.seek(0)
        
        filename = f"IELTS_Report_{analysis.get('student_name', 'Student')}_{datetime.now().strftime('%Y%m%d')}.txt"
        
        return send_file(
            buffer,
            mimetype='text/plain',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    """Analyze multiple students from CSV data"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read CSV
        import csv
        from io import StringIO
        
        content = file.read().decode('utf-8')
        reader = csv.DictReader(StringIO(content))
        
        results = []
        for row in reader:
            try:
                scores = {
                    'listening': float(row.get('listening', 0)),
                    'speaking': float(row.get('speaking', 0)),
                    'reading': float(row.get('reading', 0)),
                    'writing': float(row.get('writing', 0))
                }
                student_name = row.get('student_name', row.get('name', 'Unknown'))
                
                analysis = analyze_scores_rule_based(scores, student_name)
                results.append(analysis)
            except Exception as e:
                results.append({'error': str(e), 'row': row})
        
        return jsonify({'results': results, 'count': len(results)})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║     IELTS Score Analyzer - AI Document Summarizer            ║
║     Server running at http://localhost:5000                  ║
╚══════════════════════════════════════════════════════════════╝

To use with LLM:
  - Set OPENAI_API_KEY environment variable for GPT-4
  - Set ANTHROPIC_API_KEY environment variable for Claude

API Endpoints:
  POST /api/analyze      - Analyze single student
  POST /api/export       - Export report
  POST /api/batch-analyze - Analyze multiple students (CSV)
""")
    
    app.run(debug=True, port=5000)

