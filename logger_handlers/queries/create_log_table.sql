CREATE TABLE [etl].[log] (
[Id] [uniqueidentifier] NOT NULL,
[Thread] [varchar](255) NULL,
[Level] [varchar](50) NULL,
[Logger] [varchar](255) NULL,
[Message] [varchar](max) NULL,
[Exception] [nvarchar](max) NULL,
[CreatedOn] [datetime] NOT NULL,
[CreatedBy] [varchar](50) NOT NULL,
CONSTRAINT [PK_Log] PRIMARY KEY CLUSTERED
(
[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 80) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[Log] ADD  CONSTRAINT [DF_Log_Id]  DEFAULT (newid()) FOR [Id]
GO

ALTER TABLE [dbo].[Log] ADD  CONSTRAINT [DF_Log_CreatedOn]  DEFAULT (getdate()) FOR [CreatedOn]
GO

ALTER TABLE [dbo].[Log] ADD  CONSTRAINT [DF_Log_CreatedBy]  DEFAULT (system_user) FOR [CreatedBy]
GO
