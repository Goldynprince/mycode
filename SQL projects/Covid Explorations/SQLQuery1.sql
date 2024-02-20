SELECT *
From PortfolioProject..CovidDeaths2
where continent is not null
order by 3,4

--SELECT *
--From PortfolioProject..CovidVaccinations2
--order by 3,4

--Looking at the total cases vs total deaths


Select location, date, total_cases, total_deaths, (total_deaths/total_cases * 100) as DeathPercentage
from PortfolioProject..CovidDeaths2
where location like '%Nigeria%' and continent is not null
order by 1,2

--Looking at the total cases vs population
Select location, date, total_cases, population, (total_cases/population * 100) as InfectionPercentage
from PortfolioProject..CovidDeaths2
where location like '%Nigeria%' and continent is not null
order by 1,2

--looking at countries with highest infection rate

select location, population, Max(total_cases) as HighestInfectionCount, Max((total_cases/population)*100) as InfectionPercentage
from PortfolioProject..CovidDeaths2
where continent is not null
group by location, population
order by InfectionPercentage desc

--showing the countries with highest deathcount  per population
select location, Max(cast(total_deaths as int)) as TotalDeaths, Max((total_deaths/population)*100) as DeathPercentage
from PortfolioProject..CovidDeaths2
where continent is not null
group by location
order by TotalDeaths desc

--LETS BREAK IT DOWN BY CONTINENT
select continent, Max(cast(total_deaths as int)) as TotalDeaths, Max((total_deaths/population)*100) as DeathPercentage
from PortfolioProject..CovidDeaths2
where continent is not null
group by continent
order by TotalDeaths desc

--LETS BREAK IT DOWN BY CONTINENT
select location, Max(cast(total_deaths as int)) as TotalDeaths, Max((total_deaths/population)*100) as DeathPercentage
from PortfolioProject..CovidDeaths2
where continent is null
group by location
order by TotalDeaths desc

--	GLOBAL NUMBERS

---COVID VACCINATIONS
SELECT *
FROM PortfolioProject..CovidVaccinations2 dea
JOIN PortfolioProject..CovidVaccinations2 vac
ON dea.location = vac.location
	and dea.date = vac.date

-- Looking at total population vs vaccination
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, sum(convert(int, vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date) as RollingPeopleVaccinated
FROM PortfolioProject..CovidDeaths2 dea
JOIN PortfolioProject..CovidVaccinations2 vac
ON dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
order by 2,3

--USE CTE
with PopvsVac (continent, location, date, population, new_vaccinations, RollingPeopleVaccinated)
as
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, sum(convert(int, vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date) as RollingPeopleVaccinated
FROM PortfolioProject..CovidDeaths2 dea
JOIN PortfolioProject..CovidVaccinations2 vac
ON dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
)

select *, (RollingPeopleVaccinated/Population)*100
from PopvsVac
