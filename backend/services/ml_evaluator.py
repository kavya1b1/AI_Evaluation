from backend.services.financial_checker import check_finance

finance_result = check_finance(budget)

finance_score = finance_result["finance_score"]
violations = finance_result["violations"]

from backend.services.novelty_engine import novelty_analysis

novelty_result = novelty_analysis(text)

novelty_score = novelty_result["novelty_score"]
similar_projects = novelty_result["similar_projects"]
