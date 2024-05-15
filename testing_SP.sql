IF OBJECT_ID('tempdb..#ExecutionResults') IS NOT NULL
    DROP TABLE #ExecutionResults;

CREATE TABLE #ExecutionResults (
    RunID INT IDENTITY(1,1) PRIMARY KEY,
    ExecutionTimeMs INT,
    Status NVARCHAR(50)
);

DECLARE @StartTime DATETIME,
        @EndTime DATETIME,
        @ExecutionTimeMs INT,
        @Status NVARCHAR(50),
        @Counter INT = 1,
        @TotalRuns INT = 100;

WHILE @Counter <= @TotalRuns
BEGIN
    BEGIN TRY
        SET @StartTime = GETDATE();
        EXEC spTop10_DH1;
        SET @EndTime = GETDATE();
        SET @ExecutionTimeMs = DATEDIFF(MILLISECOND, @StartTime, @EndTime);
        SET @Status = 'Success';
    END TRY
    BEGIN CATCH
        -- In case of an error, set execution time to 0 and status to Failed
        SET @ExecutionTimeMs = 0;
        SET @Status = 'Failed';
    END CATCH
    INSERT INTO #ExecutionResults (ExecutionTimeMs, Status)
    VALUES (@ExecutionTimeMs, @Status);
    SET @Counter = @Counter + 1;
END

SELECT
    AVG(CAST(ExecutionTimeMs AS FLOAT)) AS AverageExecutionTimeMs,
    SUM(CASE WHEN Status = 'Failed' THEN 1 ELSE 0 END) AS Failures,
    COUNT(*) AS TotalRuns,
    (SUM(CASE WHEN Status = 'Failed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS FailureRatePercent
FROM 
    #ExecutionResults;

SELECT * FROM #ExecutionResults;
