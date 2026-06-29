# AI usage

AI-агент использовался как рабочий инструмент: для быстрого разбора требований, черновых вариантов структуры и проверки крайних случаев. Итоговые решения, правки и проверка результата выполнялись вручную.

## Где использовался AI

- Разбор тестового задания и выделение минимального end-to-end сценария.
- Черновой план backend-слоев: schemas, provider abstraction, service, repository.
- Список failure modes для structured output: malformed JSON, missing fields, invalid severity, provider failure.
- Черновик popup-интерфейса для Chrome Extension.
- Черновик README, который затем был сокращен и переписан под локальный запуск.

## Примеры промптов

1. Разбери требования тестового и предложи минимальный end-to-end slice на 2 дня.
2. Предложи структуру FastAPI backend для decode run, provider abstraction и Pydantic validation.
3. Составь тестовые случаи для structured output validation и provider failures.
4. Набросай React popup для Chrome Extension: textarea, run button, loading, error, copy action.
5. Проверь README на воспроизводимость: запуск backend, extension, tests, fake provider.

## Что было принято

- Разделение backend на `schemas`, `providers`, `service`, `repository`.
- Fake provider как обязательный путь для локальной проверки без API-ключа.
- Отдельные backend-тесты для Pydantic-схемы и API.
- Минимальный popup как рабочий extension slice без лишней логики.

## Что было изменено вручную

- Уточнены safe error codes и сообщения.
- Добавлено хранение raw provider output и structured result в run.
- PostgreSQL оставлен для runtime, SQLite используется только в тестах.
- WXT заменен на обычный Manifest V3 + Vite, потому что так проект проще воспроизводится локально и не тянет лишний dev tooling.
- README переписан без рекламного тона: команды запуска, API, тесты, tradeoffs.

## Что было отклонено

- Real LLM provider в рамках тестового: без API-ключа проект должен запускаться полностью локально.
- Background worker и очередь задач: для короткого прототипа достаточно popup -> backend -> result.
- Alembic в первой версии: для прототипа используется `create_all`, в production добавил бы миграции.
- Слишком широкая архитектура с workflow engine: для задания важнее законченный, проверяемый slice.

## Как проверялся результат

- `pytest` для backend.
- `npm audit --omit=dev` для extension dependencies.
- `npm run typecheck` и `npm run build` для extension.
- HTTP smoke check: decode request и чтение run по `run_id`.
- Ручной просмотр README и файлов репозитория на лишние следы и невоспроизводимые шаги.

## Найденные ограничения AI-вывода

- Первые варианты были шире, чем нужно для двухдневного тестового.
- AI предлагал подключить real LLM provider раньше, чем был готов воспроизводимый fake provider.
- README в первом варианте выглядел слишком презентационно, его пришлось сделать короче и ближе к технической документации.
