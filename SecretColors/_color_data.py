"""
All the data collected from external source will go there
"""

PALETTE_IBM = "ibm"
PALETTE_MATERIAL = "material"
PALETTE_COLOR_BREWER = "ColorBrewer"


class ParentPalette:

    def __init__(self):
        self.name = "name"
        self.value = "value"
        self.grade = "grade"
        self.core = "core"
        self.all = "all"
        self.special = "special"

    def get_colors(self):
        raise NotImplementedError

    def get_palette_name(self):
        raise NotImplementedError

    def get_grade_range(self):
        raise NotImplementedError


class IBMPalette(ParentPalette):

    def get_palette_name(self):
        return PALETTE_IBM

    def get_colors(self):
        return self.colors

    def get_grade_range(self):
        return [0, 1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    n = "name"
    v = "value"
    g = "grade"
    c = "core"
    a = "all"
    s = "special"
    colors = [
        {n: 'ultramarine', c: 60, a: [{g: 1, v: '#e7e9f7', s: False},
                                      {g: 10, v: '#d1d7f4', s: False},
                                      {g: 20, v: '#b0bef3', s: False},
                                      {g: 30, v: '#89a2f6', s: False},
                                      {g: 40, v: '#648fff', s: False},
                                      {g: 50, v: '#3c6df0', s: False},
                                      {g: 60, v: '#3151b7', s: False},
                                      {g: 70, v: '#2e3f8f', s: False},
                                      {g: 80, v: '#252e6a', s: False},
                                      {g: 90, v: '#20214f', s: False}]},
        {n: 'blue', c: 50, a: [{g: 1, v: '#e1ebf7', s: False},
                               {g: 10, v: '#c8daf4', s: False},
                               {g: 20, v: '#a8c0f3', s: False},
                               {g: 30, v: '#79a6f6', s: False},
                               {g: 40, v: '#5392ff', s: False},
                               {g: 50, v: '#2d74da', s: False},
                               {g: 60, v: '#1f57a4', s: False},
                               {g: 70, v: '#25467a', s: False},
                               {g: 80, v: '#1d3458', s: False},
                               {g: 90, v: '#19273c', s: False}]},
        {n: 'cerulean', c: 40, a: [{g: 1, v: '#deedf7', s: False},
                                   {g: 10, v: '#c2dbf4', s: False},
                                   {g: 20, v: '#95c4f3', s: False},
                                   {g: 30, v: '#56acf2', s: False},
                                   {g: 40, v: '#009bef', s: False},
                                   {g: 50, v: '#047cc0', s: False},
                                   {g: 60, v: '#175d8d', s: False},
                                   {g: 70, v: '#1c496d', s: False},
                                   {g: 80, v: '#1d364d', s: False},
                                   {g: 90, v: '#1b2834', s: False}]},
        {n: 'aqua', c: 30, a: [{g: 1, v: '#d1f0f7', s: False},
                               {g: 10, v: '#a0e3f0', s: False},
                               {g: 20, v: '#71cddd', s: False},
                               {g: 30, v: '#00b6cb', s: False},
                               {g: 40, v: '#12a3b4', s: False},
                               {g: 50, v: '#188291', s: False},
                               {g: 60, v: '#17616b', s: False},
                               {g: 70, v: '#164d56', s: False},
                               {g: 80, v: '#13393e', s: False},
                               {g: 90, v: '#122a2e', s: False}]},
        {n: 'teal', c: 40, a: [{g: 1, v: '#c0f5e8', s: False},
                               {g: 10, v: '#8ee9d4', s: False},
                               {g: 20, v: '#40d5bb', s: False},
                               {g: 30, v: '#00baa1', s: False},
                               {g: 40, v: '#00a78f', s: False},
                               {g: 50, v: '#008673', s: False},
                               {g: 60, v: '#006456', s: False},
                               {g: 70, v: '#124f44', s: False},
                               {g: 80, v: '#133a32', s: False},
                               {g: 90, v: '#122b26', s: False}]},
        {n: 'green', c: 30, a: [{g: 1, v: '#cef3d1', s: False},
                                {g: 10, v: '#89eda0', s: False},
                                {g: 20, v: '#57d785', s: False},
                                {g: 30, v: '#34bc6e', s: False},
                                {g: 40, v: '#00aa5e', s: False},
                                {g: 50, v: '#00884b', s: False},
                                {g: 60, v: '#116639', s: False},
                                {g: 70, v: '#12512e', s: False},
                                {g: 80, v: '#123b22', s: False},
                                {g: 90, v: '#112c1b', s: False}]},
        {n: 'lime', c: 20, a: [{g: 1, v: '#d7f4bd', s: False},
                               {g: 10, v: '#b4e876', s: False},
                               {g: 20, v: '#95d13c', s: False},
                               {g: 30, v: '#81b532', s: False},
                               {g: 40, v: '#73a22c', s: False},
                               {g: 50, v: '#5b8121', s: False},
                               {g: 60, v: '#426200', s: False},
                               {g: 70, v: '#374c1a', s: False},
                               {g: 80, v: '#283912', s: False},
                               {g: 90, v: '#1f2a10', s: False}]},
        {n: 'yellow', c: 10, a: [{g: 1, v: '#fbeaae', s: False},
                                 {g: 10, v: '#fed500', s: False},
                                 {g: 20, v: '#e3bc13', s: False},
                                 {g: 30, v: '#c6a21a', s: False},
                                 {g: 40, v: '#b3901f', s: False},
                                 {g: 50, v: '#91721f', s: False},
                                 {g: 60, v: '#70541b', s: False},
                                 {g: 70, v: '#5b421a', s: False},
                                 {g: 80, v: '#452f18', s: False},
                                 {g: 90, v: '#372118', s: False}]},
        {n: 'gold', c: 20, a: [{g: 1, v: '#f5e8db', s: False},
                               {g: 10, v: '#ffd191', s: False},
                               {g: 20, v: '#ffb000', s: False},
                               {g: 30, v: '#e39d14', s: False},
                               {g: 40, v: '#c4881c', s: False},
                               {g: 50, v: '#9c6d1e', s: False},
                               {g: 60, v: '#74521b', s: False},
                               {g: 70, v: '#5b421c', s: False},
                               {g: 80, v: '#42301b', s: False},
                               {g: 90, v: '#2f261c', s: False}]},
        {n: 'orange', c: 30, a: [{g: 1, v: '#f5e8de', s: False},
                                 {g: 10, v: '#fdcfad', s: False},
                                 {g: 20, v: '#fcaf6d', s: False},
                                 {g: 30, v: '#fe8500', s: False},
                                 {g: 40, v: '#db7c00', s: False},
                                 {g: 50, v: '#ad6418', s: False},
                                 {g: 60, v: '#814b19', s: False},
                                 {g: 70, v: '#653d1b', s: False},
                                 {g: 80, v: '#482e1a', s: False},
                                 {g: 90, v: '#33241c', s: False}]},
        {n: 'peach', c: 40, a: [{g: 1, v: '#f7e7e2', s: False},
                                {g: 10, v: '#f8d0c3', s: False},
                                {g: 20, v: '#faad96', s: False},
                                {g: 30, v: '#fc835c', s: False},
                                {g: 40, v: '#fe6100', s: False},
                                {g: 50, v: '#c45433', s: False},
                                {g: 60, v: '#993a1d', s: False},
                                {g: 70, v: '#782f1c', s: False},
                                {g: 80, v: '#56251a', s: False},
                                {g: 90, v: '#3a201b', s: False}]},
        {n: 'red', c: 50, a: [{g: 1, v: '#f7e6e6', s: False},
                              {g: 10, v: '#fccec7', s: False},
                              {g: 20, v: '#ffaa9d', s: False},
                              {g: 30, v: '#ff806c', s: False},
                              {g: 40, v: '#ff5c49', s: False},
                              {g: 50, v: '#e62325', s: False},
                              {g: 60, v: '#aa231f', s: False},
                              {g: 70, v: '#83231e', s: False},
                              {g: 80, v: '#5c1f1b', s: False},
                              {g: 90, v: '#3e1d1b', s: False}]},
        {n: 'magenta', c: 40, a: [{g: 1, v: '#f5e7eb', s: False},
                                  {g: 10, v: '#f5cedb', s: False},
                                  {g: 20, v: '#f7aac3', s: False},
                                  {g: 30, v: '#f87eac', s: False},
                                  {g: 40, v: '#ff509e', s: False},
                                  {g: 50, v: '#dc267f', s: False},
                                  {g: 60, v: '#a91560', s: False},
                                  {g: 70, v: '#831b4c', s: False},
                                  {g: 80, v: '#5d1a38', s: False},
                                  {g: 90, v: '#401a29', s: False}]},
        {n: 'purple', c: 50, a: [{g: 1, v: '#f7e4fb', s: False},
                                 {g: 10, v: '#efcef3', s: False},
                                 {g: 20, v: '#e4adea', s: False},
                                 {g: 30, v: '#d68adf', s: False},
                                 {g: 40, v: '#cb71d7', s: False},
                                 {g: 50, v: '#c22dd5', s: False},
                                 {g: 60, v: '#9320a2', s: False},
                                 {g: 70, v: '#71237c', s: False},
                                 {g: 80, v: '#501e58', s: False},
                                 {g: 90, v: '#3b1a40', s: False}]},
        {n: 'violet', c: 60, a: [{g: 1, v: '#ece8f5', s: False},
                                 {g: 10, v: '#e2d2f4', s: False},
                                 {g: 20, v: '#d2b5f0', s: False},
                                 {g: 30, v: '#bf93eb', s: False},
                                 {g: 40, v: '#b07ce8', s: False},
                                 {g: 50, v: '#9753e1', s: False},
                                 {g: 60, v: '#7732bb', s: False},
                                 {g: 70, v: '#602797', s: False},
                                 {g: 80, v: '#44216a', s: False},
                                 {g: 90, v: '#321c4c', s: False}]},
        {n: 'indigo', c: 70, a: [{g: 1, v: '#e9e8ff', s: False},
                                 {g: 10, v: '#dcd4f7', s: False},
                                 {g: 20, v: '#c7b6f7', s: False},
                                 {g: 30, v: '#ae97f4', s: False},
                                 {g: 40, v: '#9b82f3', s: False},
                                 {g: 50, v: '#785ef0', s: False},
                                 {g: 60, v: '#5a3ec8', s: False},
                                 {g: 70, v: '#473793', s: False},
                                 {g: 80, v: '#352969', s: False},
                                 {g: 90, v: '#272149', s: False}]},
        {n: 'gray', c: 50, a: [{g: 1, v: '#eaeaea', s: False},
                               {g: 10, v: '#d8d8d8', s: False},
                               {g: 20, v: '#c0bfc0', s: False},
                               {g: 30, v: '#a6a5a6', s: False},
                               {g: 40, v: '#949394', s: False},
                               {g: 50, v: '#777677', s: False},
                               {g: 60, v: '#595859', s: False},
                               {g: 70, v: '#464646', s: False},
                               {g: 80, v: '#343334', s: False},
                               {g: 90, v: '#272727', s: False}]},
        {n: 'cool-gray', c: 50, a: [{g: 1, v: '#e3ecec', s: False},
                                    {g: 10, v: '#d0dada', s: False},
                                    {g: 20, v: '#b8c1c1', s: False},
                                    {g: 30, v: '#9fa7a7', s: False},
                                    {g: 40, v: '#8c9696', s: False},
                                    {g: 50, v: '#6f7878', s: False},
                                    {g: 60, v: '#535a5a', s: False},
                                    {g: 70, v: '#424747', s: False},
                                    {g: 80, v: '#343334', s: False},
                                    {g: 90, v: '#272727', s: False}]},
        {n: 'warm-gray', c: 50, a: [{g: 1, v: '#efe9e9', s: False},
                                    {g: 10, v: '#e2d5d5', s: False},
                                    {g: 20, v: '#ccbcbc', s: False},
                                    {g: 30, v: '#b4a1a1', s: False},
                                    {g: 40, v: '#9e9191', s: False},
                                    {g: 50, v: '#7d7373', s: False},
                                    {g: 60, v: '#5f5757', s: False},
                                    {g: 70, v: '#4b4545', s: False},
                                    {g: 80, v: '#373232', s: False},
                                    {g: 90, v: '#2a2626', s: False}]},
        {n: 'neutral-white', c: 1, a: [{g: 1, v: '#fcfcfc', s: False},
                                       {g: 2, v: '#f9f9f9', s: False},
                                       {g: 3, v: '#f6f6f6', s: False},
                                       {g: 4, v: '#f3f3f3',
                                        s: False}]},
        {n: 'cool-white', c: 1, a: [{g: 1, v: '#fbfcfc', s: False},
                                    {g: 2, v: '#f8fafa', s: False},
                                    {g: 3, v: '#f4f7f7', s: False},
                                    {g: 4, v: '#f0f4f4', s: False}]},
        {n: 'warm-white', c: 1, a: [{g: 1, v: '#fdfcfc', s: False},
                                    {g: 2, v: '#fbf8f8', s: False},
                                    {g: 3, v: '#f9f6f6', s: False},
                                    {g: 4, v: '#f6f3f3', s: False}]},
        {n: 'black', c: 100, a: [{g: 100, v: '#000000', s: False}]},
        {n: 'white', c: 0, a: [{g: 0, v: '#ffffff', s: False}]}
    ]


class MaterialPalette(ParentPalette):

    def get_grade_range(self):
        return [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    def get_palette_name(self):
        return PALETTE_MATERIAL

    def get_colors(self):
        return self.colors

    n = "name"
    v = "value"
    g = "grade"
    c = "core"
    a = "all"
    s = "special"

    colors = [
        {n: 'red', c: 700, a: [
            {g: 50, v: '#ffebee', s: False},
            {g: 100, v: '#ffcdd2', s: False},
            {g: 200, v: '#ef9a9a', s: False},
            {g: 300, v: '#e57373', s: False},
            {g: 400, v: '#ef5350', s: False},
            {g: 500, v: '#f44336', s: False},
            {g: 600, v: '#e53935', s: False},
            {g: 700, v: '#d32f2f', s: False},
            {g: 800, v: '#c62828', s: False},
            {g: 900, v: '#b71c1c', s: False},
            {g: 100, v: '#ff8a80', s: True},
            {g: 200, v: '#ff5252', s: True},
            {g: 400, v: '#ff1744', s: True},
            {g: 700, v: '#d50000', s: True}]},
        {n: 'pink', c: 700, a: [
            {g: 50, v: '#fce4ec', s: False},
            {g: 100, v: '#f8bbd0', s: False},
            {g: 200, v: '#f48fb1', s: False},
            {g: 300, v: '#f06292', s: False},
            {g: 400, v: '#ec407a', s: False},
            {g: 500, v: '#e91e63', s: False},
            {g: 600, v: '#d81b60', s: False},
            {g: 700, v: '#c2185b', s: False},
            {g: 800, v: '#ad1457', s: False},
            {g: 900, v: '#880e4f', s: False},
            {g: 100, v: '#ff80ab', s: True},
            {g: 200, v: '#ff4081', s: True},
            {g: 400, v: '#f50057', s: True},
            {g: 700, v: '#c51162', s: True}]},
        {n: 'purple', c: 700, a: [
            {g: 50, v: '#f3e5f5', s: False},
            {g: 100, v: '#e1bee7', s: False},
            {g: 200, v: '#ce93d8', s: False},
            {g: 300, v: '#ba68c8', s: False},
            {g: 400, v: '#ab47bc', s: False},
            {g: 500, v: '#9c27b0', s: False},
            {g: 600, v: '#8e24aa', s: False},
            {g: 700, v: '#7b1fa2', s: False},
            {g: 800, v: '#6a1b9a', s: False},
            {g: 900, v: '#4a148c', s: False},
            {g: 100, v: '#ea80fc', s: True},
            {g: 200, v: '#e040fb', s: True},
            {g: 400, v: '#d500f9', s: True},
            {g: 700, v: '#aa00ff', s: True}]},

        {n: 'deep-purple', c: 700, a: [
            {g: 50, v: '#ede7f6', s: False},
            {g: 100, v: '#d1c4e9', s: False},
            {g: 200, v: '#b39ddb', s: False},
            {g: 300, v: '#9575cd', s: False},
            {g: 400, v: '#7e57c2', s: False},
            {g: 500, v: '#673ab7', s: False},
            {g: 600, v: '#5e35b1', s: False},
            {g: 700, v: '#512da8', s: False},
            {g: 800, v: '#4527a0', s: False},
            {g: 900, v: '#311b92', s: False},
            {g: 100, v: '#b388ff', s: True},
            {g: 200, v: '#7c4dff', s: True},
            {g: 400, v: '#651fff', s: True},
            {g: 700, v: '#6200ea', s: True}]},

        {n: 'indigo', c: 700, a: [
            {g: 50, v: '#e8eaf6', s: False},
            {g: 100, v: '#c5cae9', s: False},
            {g: 200, v: '#9fa8da', s: False},
            {g: 300, v: '#7986cb', s: False},
            {g: 400, v: '#5c6bc0', s: False},
            {g: 500, v: '#3f51b5', s: False},
            {g: 600, v: '#3949ab', s: False},
            {g: 700, v: '#303f9f', s: False},
            {g: 800, v: '#283593', s: False},
            {g: 900, v: '#1a237e', s: False},
            {g: 100, v: '#8c9eff', s: True},
            {g: 200, v: '#536dfe', s: True},
            {g: 400, v: '#3d5afe', s: True},
            {g: 700, v: '#304ffe', s: True}]},

        {n: 'blue', c: 700, a: [
            {g: 50, v: '#e3f2fd', s: False},
            {g: 100, v: '#bbdefb', s: False},
            {g: 200, v: '#90caf9', s: False},
            {g: 300, v: '#64b5f6', s: False},
            {g: 400, v: '#42a5f5', s: False},
            {g: 500, v: '#2196f3', s: False},
            {g: 600, v: '#1e88e5', s: False},
            {g: 700, v: '#1976d2', s: False},
            {g: 800, v: '#1565c0', s: False},
            {g: 900, v: '#0d47a1', s: False},
            {g: 100, v: '#82b1ff', s: True},
            {g: 200, v: '#448aff', s: True},
            {g: 400, v: '#2979ff', s: True},
            {g: 700, v: '#2962ff', s: True}]},

        {n: 'light-blue', c: 700, a: [
            {g: 50, v: '#e1f5fe', s: False},
            {g: 100, v: '#b3e5fc', s: False},
            {g: 200, v: '#81d4fa', s: False},
            {g: 300, v: '#4fc3f7', s: False},
            {g: 400, v: '#29b6f6', s: False},
            {g: 500, v: '#03a9f4', s: False},
            {g: 600, v: '#039be5', s: False},
            {g: 700, v: '#0288d1', s: False},
            {g: 800, v: '#0277bd', s: False},
            {g: 900, v: '#01579b', s: False},
            {g: 100, v: '#80d8ff', s: True},
            {g: 200, v: '#40c4ff', s: True},
            {g: 400, v: '#00b0ff', s: True},
            {g: 700, v: '#0091ea', s: True}]},

        {n: 'cyan', c: 700, a: [
            {g: 50, v: '#e0f7fa', s: False},
            {g: 100, v: '#b2ebf2', s: False},
            {g: 200, v: '#80deea', s: False},
            {g: 300, v: '#4dd0e1', s: False},
            {g: 400, v: '#26c6da', s: False},
            {g: 500, v: '#00bcd4', s: False},
            {g: 600, v: '#00acc1', s: False},
            {g: 700, v: '#0097a7', s: False},
            {g: 800, v: '#00838f', s: False},
            {g: 900, v: '#006064', s: False},
            {g: 100, v: '#84ffff', s: True},
            {g: 200, v: '#18ffff', s: True},
            {g: 400, v: '#00e5ff', s: True},
            {g: 700, v: '#00b8d4', s: True}]},

        {n: 'teal', c: 700, a: [
            {g: 50, v: '#e0f2f1', s: False},
            {g: 100, v: '#b2dfdb', s: False},
            {g: 200, v: '#80cbc4', s: False},
            {g: 300, v: '#4db6ac', s: False},
            {g: 400, v: '#26a69a', s: False},
            {g: 500, v: '#009688', s: False},
            {g: 600, v: '#00897b', s: False},
            {g: 700, v: '#00796b', s: False},
            {g: 800, v: '#00695c', s: False},
            {g: 900, v: '#004d40', s: False},
            {g: 100, v: '#a7ffeb', s: True},
            {g: 200, v: '#64ffda', s: True},
            {g: 400, v: '#1de9b6', s: True},
            {g: 700, v: '#00bfa5', s: True}]},

        {n: 'green', c: 700, a: [
            {g: 50, v: '#e8f5e9', s: False}, {g: 100, v: '#c8e6c9', s: False},
            {g: 200, v: '#a5d6a7', s: False}, {g: 300, v: '#81c784', s: False},
            {g: 400, v: '#66bb6a', s: False}, {g: 500, v: '#4caf50', s: False},
            {g: 600, v: '#43a047', s: False}, {g: 700, v: '#388e3c', s: False},
            {g: 800, v: '#2e7d32', s: False}, {g: 900, v: '#1b5e20', s: False},
            {g: 100, v: '#b9f6ca', s: True}, {g: 200, v: '#69f0ae', s: True},
            {g: 400, v: '#00e676', s: True}, {g: 700, v: '#00c853', s: True}]},

        {n: 'light-green', c: 700, a: [
            {g: 50, v: '#f1f8e9', s: False}, {g: 100, v: '#dcedc8', s: False},
            {g: 200, v: '#c5e1a5', s: False},
            {g: 300, v: '#aed581', s: False},
            {g: 400, v: '#9ccc65', s: False},
            {g: 500, v: '#8bc34a', s: False},
            {g: 600, v: '#7cb342', s: False},
            {g: 700, v: '#689f38', s: False},
            {g: 800, v: '#558b2f', s: False},
            {g: 900, v: '#33691e', s: False},
            {g: 100, v: '#ccff90', s: True},
            {g: 200, v: '#b2ff59', s: True},
            {g: 400, v: '#76ff03', s: True},
            {g: 700, v: '#64dd17', s: True}]},

        {n: 'lime', c: 700, a: [
            {g: 50, v: '#f9fbe7', s: False},
            {g: 100, v: '#f0f4c3', s: False},
            {g: 200, v: '#e6ee9c', s: False},
            {g: 300, v: '#dce775', s: False},
            {g: 400, v: '#d4e157', s: False},
            {g: 500, v: '#cddc39', s: False},
            {g: 600, v: '#c0ca33', s: False},
            {g: 700, v: '#afb42b', s: False},
            {g: 800, v: '#9e9d24', s: False},
            {g: 900, v: '#827717', s: False},
            {g: 100, v: '#f4ff81', s: True},
            {g: 200, v: '#eeff41', s: True},
            {g: 400, v: '#c6ff00', s: True},
            {g: 700, v: '#aeea00', s: True}]},

        {n: 'yellow', c: 700, a: [
            {g: 50, v: '#fffde7', s: False},
            {g: 100, v: '#fff9c4', s: False},
            {g: 200, v: '#fff59d', s: False},
            {g: 300, v: '#fff176', s: False},
            {g: 400, v: '#ffee58', s: False},
            {g: 500, v: '#ffeb3b', s: False},
            {g: 600, v: '#fdd835', s: False},
            {g: 700, v: '#fbc02d', s: False},
            {g: 800, v: '#f9a825', s: False},
            {g: 900, v: '#f57f17', s: False},
            {g: 100, v: '#ffff8d', s: True},
            {g: 200, v: '#ffff00', s: True},
            {g: 400, v: '#ffea00', s: True},
            {g: 700, v: '#ffd600', s: True}]},

        {n: 'amber', c: 700, a: [
            {g: 50, v: '#fff8e1', s: False},
            {g: 100, v: '#ffecb3', s: False},
            {g: 200, v: '#ffe082', s: False},
            {g: 300, v: '#ffd54f', s: False},
            {g: 400, v: '#ffca28', s: False},
            {g: 500, v: '#ffc107', s: False},
            {g: 600, v: '#ffb300', s: False},
            {g: 700, v: '#ffa000', s: False},
            {g: 800, v: '#ff8f00', s: False},
            {g: 900, v: '#ff6f00', s: False},
            {g: 100, v: '#ffe57f', s: True},
            {g: 200, v: '#ffd740', s: True},
            {g: 400, v: '#ffc400', s: True},
            {g: 700, v: '#ffab00', s: True}]},

        {n: 'orange', c: 700, a: [
            {g: 50, v: '#fff3e0', s: False},
            {g: 100, v: '#ffe0b2', s: False},
            {g: 200, v: '#ffcc80', s: False},
            {g: 300, v: '#ffb74d', s: False},
            {g: 400, v: '#ffa726', s: False},
            {g: 500, v: '#ff9800', s: False},
            {g: 600, v: '#fb8c00', s: False},
            {g: 700, v: '#f57c00', s: False},
            {g: 800, v: '#ef6c00', s: False},
            {g: 900, v: '#e65100', s: False},
            {g: 100, v: '#ffd180', s: True},
            {g: 200, v: '#ffab40', s: True},
            {g: 400, v: '#ff9100', s: True},
            {g: 700, v: '#ff6d00', s: True}]},

        {n: 'deep-orange', c: 700, a: [
            {g: 50, v: '#fbe9e7', s: False},
            {g: 100, v: '#ffccbc', s: False},
            {g: 200, v: '#ffab91', s: False},
            {g: 300, v: '#ff8a65', s: False},
            {g: 400, v: '#ff7043', s: False},
            {g: 500, v: '#ff5722', s: False},
            {g: 600, v: '#f4511e', s: False},
            {g: 700, v: '#e64a19', s: False},
            {g: 800, v: '#d84315', s: False},
            {g: 900, v: '#bf360c', s: False},
            {g: 100, v: '#ff9e80', s: True},
            {g: 200, v: '#ff6e40', s: True},
            {g: 400, v: '#ff3d00', s: True},
            {g: 700, v: '#dd2c00', s: True}]},

        {n: 'brown', c: 700, a: [
            {g: 50, v: '#efebe9', s: False},
            {g: 100, v: '#d7ccc8', s: False},
            {g: 200, v: '#bcaaa4', s: False},
            {g: 300, v: '#a1887f', s: False},
            {g: 400, v: '#8d6e63', s: False},
            {g: 500, v: '#795548', s: False},
            {g: 600, v: '#6d4c41', s: False},
            {g: 700, v: '#5d4037', s: False},
            {g: 800, v: '#4e342e', s: False},
            {g: 900, v: '#3e2723', s: False}]},

        {n: 'gray', c: 700, a: [
            {g: 50, v: '#fafafa', s: False},
            {g: 100, v: '#f5f5f5', s: False},
            {g: 200, v: '#eeeeee', s: False},
            {g: 300, v: '#e0e0e0', s: False},
            {g: 400, v: '#bdbdbd', s: False},
            {g: 500, v: '#9e9e9e', s: False},
            {g: 600, v: '#757575', s: False},
            {g: 700, v: '#616161', s: False},
            {g: 800, v: '#424242', s: False},
            {g: 900, v: '#212121', s: False}]},

        {n: 'blue-gray', c: 700, a: [
            {g: 50, v: '#eceff1', s: False},
            {g: 100, v: '#cfd8dc', s: False},
            {g: 200, v: '#b0bec5', s: False},
            {g: 300, v: '#90a4ae', s: False},
            {g: 400, v: '#78909c', s: False},
            {g: 500, v: '#607d8b', s: False},
            {g: 600, v: '#546e7a', s: False},
            {g: 700, v: '#455a64', s: False},
            {g: 800, v: '#37474f', s: False},
            {g: 900, v: '#263238', s: False}]},
        {n: 'black', c: 1000, a: [{g: 1000, v: '#000000', s: False}]},
        {n: 'white', c: 0, a: [{g: 0, v: '#ffffff', s: False}]}
    ]