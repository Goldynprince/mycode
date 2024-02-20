select * from PortfolioProject..[NashvilleHousing]
-- Standardize the date format
select SaleDate, convert(Date,SaleDate) 
from PortfolioProject..[NashvilleHousing]

Update PortfolioProject..[NashvilleHousing]
set SaleDate = convert(Date,SaleDate) 

Alter table PortfolioProject..[NashvilleHousing]
Add SaleDateConverted Date;

Update PortfolioProject..[NashvilleHousing]
set SaleDateConverted = convert(Date,SaleDate) 

select SaleDateConverted
from PortfolioProject..[NashvilleHousing]

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- Populate property address
select *
from PortfolioProject..[NashvilleHousing]
where PropertyAddress is null

select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, isnull(a.PropertyAddress, b.PropertyAddress)
from PortfolioProject..[NashvilleHousing] a
join PortfolioProject..[NashvilleHousing] b
	on a.ParcelID = b.ParcelID
	and a.UniqueID <> b.UniqueID
	where a.PropertyAddress is null

Update a
set PropertyAddress = isnull(a.PropertyAddress, b.PropertyAddress)
from PortfolioProject..[NashvilleHousing] a
join PortfolioProject..[NashvilleHousing] b
	on a.ParcelID = b.ParcelID
	and a.UniqueID <> b.UniqueID
	where a.PropertyAddress is null

-- breaking out address into individual columns
select PropertyAddress
From PortfolioProject..NashvilleHousing

select
substring(PropertyAddress, 1, Charindex(',', PropertyAddress) - 1) as Address,
substring(PropertyAddress, Charindex(',', PropertyAddress) + 1, Len(PropertyAddress)) as Address
From PortfolioProject..[NashvilleHousing]

Alter table PortfolioProject..[NashvilleHousing]
Add PropertySplitAddress Nvarchar(255);

Alter table PortfolioProject..[NashvilleHousing]
Add PropertySplitCity Nvarchar(255);
;

Update PortfolioProject..[NashvilleHousing]
set PropertySplitAddress = substring(PropertyAddress, 1, Charindex(',', PropertyAddress) - 1);

Update PortfolioProject..[NashvilleHousing]
set PropertySplitCity = substring(PropertyAddress, Charindex(',', PropertyAddress) + 1, Len(PropertyAddress));


select PropertySplitAddress, PropertySplitCity
From PortfolioProject..NashvilleHousing


--OwnerAddress
select OwnerAddress
From PortfolioProject..NashvilleHousing

select
Parsename(REPLACE(OwnerAddress, ',', '.'), 1),
Parsename(REPLACE(OwnerAddress, ',', '.'), 2), 
Parsename(REPLACE(OwnerAddress, ',', '.'), 3)

From PortfolioProject..NashvilleHousing

Alter table PortfolioProject..[NashvilleHousing]
Add OwnerSplitAddress Nvarchar(255);

Alter table PortfolioProject..[NashvilleHousing]
Add OwnerSplitCity Nvarchar(255);

Alter table PortfolioProject..[NashvilleHousing]
Add OwnerSplitState Nvarchar(255);;

Update PortfolioProject..[NashvilleHousing]
set OwnerSplitAddress = Parsename(REPLACE(OwnerAddress, ',', '.'), 3);

Update PortfolioProject..[NashvilleHousing]
set OwnerSplitCity = Parsename(REPLACE(OwnerAddress, ',', '.'), 2);

Update PortfolioProject..[NashvilleHousing]
set OwnerSplitState = Parsename(REPLACE(OwnerAddress, ',', '.'), 1);



-- Change Y and N to yes and no
select distinct(SoldAsVacant), Count(SoldAsVacant)
From PortfolioProject..[NashvilleHousing]
group by SoldAsVacant
order by 2 desc

select SoldAsVacant, 

CASE WHEN SoldAsVacant = 'Y' THEN 'YES'
	WHEN SoldAsVacant = 'N' THEN 'NO'
	ELSE SoldAsVacant
	END

From PortfolioProject..[NashvilleHousing]

Update PortfolioProject..[NashvilleHousing]
set SoldAsVacant = CASE WHEN SoldAsVacant = 'Y' THEN 'YES'
	WHEN SoldAsVacant = 'N' THEN 'NO'
	ELSE SoldAsVacant
	END
);

-- remove duplicates
with rowNumCTE

as
(
SELECT *, 
	ROW_NUMBER() over(
		partition by ParcelID,
					 PropertyAddress, 
					 SalePrice, 
					 SaleDate, 
					 LegalReference
					 Order by 
						UniqueID)  row_num
From PortfolioProject..[NashvilleHousing]
)
Delete
from rowNumCTE
where row_num >1
--order by PropertyAddress


-- delete unused columns
alter table PortfolioProject..[NashvilleHousing]
drop column OwnerAddress, TaxDistrict, PropertyAddress, SaleDate

-- using openrowset and bulk insert rank and order rank
