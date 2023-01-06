packagedir = tgbot
testdir = tests


# *** Clean & Build ************************************************************

clean: clean-build clean-pyc clean-test  ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	@rm -fr build/
	@rm -fr dist/
	@rm -fr .eggs/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	@rm -f .coverage
	@rm -fr htmlcov/
	@rm -fr .mypy_cache
	@rm -fr .pytest_cache
	@rm -f coverage.xml
	@rm -f report.xml


# *** Lint *********************************************************************


bandit:
	@echo "running bandit (code security)"
	@bandit --recursive --silent $(packagedir)

safety:
	@echo "running safety (vulnerable dependency versions)"
	@safety check --bare -i 51946

radon:
	@echo "running radon (code complexity)"
	@! radon cc $(packagedir) -a -nc | grep .

flake8:
	@echo "running flake8 (code style)"
	@flake8 $(packagedir) $(testdir)

isort:
	@echo "running isort (imports order)"
	@isort --check-only --diff --quiet $(packagedir) $(testdir)

mypy:
	@echo "running mypy (type checking)"
	@mypy $(packagedir) $(testdir) --install-types --non-interactive --pretty \
		--ignore-missing-imports --no-error-summary


lint: bandit safety radon flake8 isort
	@true

ci: clean lint migration test
	@true

# *** Telegram bot *************************************************************

define SET_WEBHOOK_PYSCRIPT
import sys
import urllib3

bot_token, api_url = sys.argv[1], sys.argv[2]
http = urllib3.PoolManager()
r = http.request(
	"GET",
	f"https://api.telegram.org/bot{bot_token}/setWebHook?url={api_url}"
)
if r.status == 200:
	print(f"`{api_url}` set as webhook url for your bot successfully")
else:
	print(f"Unsuccessful response during registering the bot webhook"
		  f"{r.data.decode('UTF-8')}")
	exit(-1)
endef
export SET_WEBHOOK_PYSCRIPT
SET_WEBHOOK := python -c "$$SET_WEBHOOK_PYSCRIPT"

define GET_WEBHOOK_PYSCRIPT
import sys
import urllib3

bot_token = sys.argv[1]
http = urllib3.PoolManager()
r = http.request(
	"GET",
	f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
)
if r.status == 200:
	print(f"{r.data.decode('UTF-8')}")
else:
	print(f"Unsuccessful response during geting the bot webhook"
		  f"{r.data.decode('UTF-8')}")
	exit(-1)
endef
export GET_WEBHOOK_PYSCRIPT
GET_WEBHOOK := python -c "$$GET_WEBHOOK_PYSCRIPT"

register-tg-webhook:
	$(SET_WEBHOOK) $(token) $(url)

get-webhook:
	$(GET_WEBHOOK) $(token)
