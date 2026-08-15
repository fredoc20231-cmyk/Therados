from typing import Optional, Any, Dict, List
from neo4j import AsyncGraphDatabase, AsyncDriver
from therados.config.settings import settings
import logging

logger = logging.getLogger("therados.db.neo4j")

class Neo4jClient:
    def __init__(self) -> None:
        self._driver: Optional[AsyncDriver] = None

    async def connect(self) -> None:
        try:
            self._driver = AsyncGraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
        except Exception as e:
            logger.warning(f"Neo4j connection failed: {e}. Graph DB operations will report unavailable.")

    async def close(self) -> None:
        if self._driver:
            await self._driver.close()

    async def query(self, query_str: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not self._driver:
            return []
        try:
            async with self._driver.session() as session:
                result = await session.run(query_str, parameters or {})
                records = await result.data()
                return records
        except Exception as e:
            logger.error(f"Neo4j query error: {e}")
            return []

neo4j_client = Neo4jClient()
